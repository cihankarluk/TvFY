from collections import defaultdict
from typing import Any

from django.db.models import Max, Min, Avg, Sum

from TvFY.core.exceptions import MovieNotFoundError, SeriesNotFoundError
from TvFY.movies.models import Movie
from TvFY.series.models import Series, Season
from TvFY.user.models import Account, UserMovies, UserSeries


class UserService:

    @classmethod
    def create_or_update_user_movie(cls, user: Account, request_data: dict[str, Any]) -> UserMovies:
        if movie := Movie.objects.filter(tvfy_code=request_data["tvfy_code"]):
            movie = movie.get()
            user_movie = UserMovies.objects.filter(
                user=user,
                movie=movie,
            )
            if user_movie.exists():
                user_movie = user_movie.get()
                user_movie.is_watched = request_data["is_watched"]
                user_movie.is_going_to_watch = request_data["is_going_to_watch"]
                user_movie.save()
            else:
                user_movie = UserMovies.objects.create(
                    user=user,
                    movie=movie,
                    is_watched=request_data["is_watched"],
                    is_going_to_watch=request_data["is_going_to_watch"],
                )
            return user_movie
        else:
            raise MovieNotFoundError(f"Movie not exists with {request_data['tvfy_code']} tvfy_code.")

    @classmethod
    def get_movies(cls, user: Account):
        query = UserMovies.objects.select_related(
            "movie"
        ).prefetch_related(
            "movie__genres", "movie__language", "movie__country",
        ).filter(user=user)

        if user_movies := query:
            watched_movies = user_movies.filter(is_watched=True)
            aggregation_results = watched_movies.aggregate(
                Max("movie__imdb_rate"),
                Min("movie__imdb_rate"),
                Avg("movie__imdb_rate"),
                Max("movie__rt_audience_rate"),
                Min("movie__rt_audience_rate"),
                Avg("movie__rt_audience_rate"),
                Max("movie__rt_tomatometer_rate"),
                Min("movie__rt_tomatometer_rate"),
                Avg("movie__rt_tomatometer_rate"),
                Max("movie__metacritic_score"),
                Min("movie__metacritic_score"),
                Avg("movie__metacritic_score"),
                Max("movie__release_date"),
                Min("movie__release_date"),
                Sum("movie__run_time"),
            )

            genres = defaultdict(int)
            countries = defaultdict(int)
            languages = defaultdict(int)
            for watched_user_movie in watched_movies:
                for genre in watched_user_movie.movie.genres.all():
                    genres[genre.name] += 1

                for country in watched_user_movie.movie.country.all():
                    countries[country.name] += 1

                for language in watched_user_movie.movie.language.all():
                    languages[language.name] += watched_user_movie.movie.run_time

            results = {
                "max_imdb_rate": aggregation_results["movie__imdb_rate__max"],
                "min_imdb_rate": aggregation_results["movie__imdb_rate__min"],
                "avg_imdb_rate": aggregation_results["movie__imdb_rate__avg"],
                "max_rt_audience_rate": aggregation_results["movie__rt_audience_rate__max"],
                "min_rt_audience_rate": aggregation_results["movie__rt_audience_rate__min"],
                "avg_rt_audience_rate": aggregation_results["movie__rt_audience_rate__avg"],
                "max_rt_tomatometer_rate": aggregation_results["movie__rt_tomatometer_rate__max"],
                "min_rt_tomatometer_rate": aggregation_results["movie__rt_tomatometer_rate__min"],
                "avg_rt_tomatometer_rate": aggregation_results["movie__rt_tomatometer_rate__avg"],
                "max_metacritic_score": aggregation_results["movie__metacritic_score__max"],
                "min_metacritic_score": aggregation_results["movie__metacritic_score__min"],
                "avg_metacritic_score": aggregation_results["movie__metacritic_score__avg"],
                "newest_movie_watched": aggregation_results["movie__release_date__max"],
                "oldest_movie_watched": aggregation_results["movie__release_date__min"],
                "time_spent": aggregation_results["movie__run_time__sum"],
                "genres": sorted([{
                    "genre": genre,
                    "count": count
                } for genre, count in genres.items()], key=lambda d: d["count"], reverse=True
                ) if genres else [],
                "countries": sorted([{
                    "country": country,
                    "count": count
                } for country, count in countries.items()], key=lambda d: d["count"], reverse=True
                ) if countries else [],
                "languages": sorted([{
                    "country": language,
                    "time_spent": time_spent
                } for language, time_spent in languages.items()], key=lambda d: d["time_spent"], reverse=True
                ) if languages else [],
                "watched_movies": watched_movies,
                "watch_list": user_movies.filter(is_going_to_watch=True),
            }

            return results

    @classmethod
    def update_user_series(
            cls,
            user_series: UserSeries,
            last_watched_episode: int,
            request_data: dict[str, Any]
    ) -> UserSeries:
        user_series.last_watched_episode = last_watched_episode
        user_series.is_watched = request_data["is_watched"]
        user_series.is_going_to_watch = request_data["is_going_to_watch"]
        user_series.save()

        return user_series

    @classmethod
    def create_user_series(
            cls,
            user: Account,
            series: Series,
            watched_season: Season,
            last_watched_episode: int,
            request_data: dict[str, Any]
    ) -> UserSeries:
        user_series = UserSeries.objects.create(
            user=user,
            series=series,
            watched_season=watched_season,
            last_watched_episode=last_watched_episode,
            is_watched=request_data["is_watched"],
            is_going_to_watch=request_data["is_going_to_watch"],
        )
        return user_series

    @classmethod
    def create_or_update_user_series(cls, user: Account, request_data: dict[str, Any]) -> list[UserSeries]:
        results = []
        if series := Series.objects.prefetch_related("season_set").filter(tvfy_code=request_data["tvfy_code"]):
            series = series.get()
            seasons = series.season_set.all()

            if request_data["watched_past_seasons"]:
                # Add all past seasons till given season.
                for season in range(1, int(request_data["watched_season"]) + 1):
                    watched_season = seasons.get(season=str(season))
                    last_watched_episode = watched_season.episode_set.count()
                    if season == request_data["watched_season"]:
                        last_watched_episode = request_data["last_watched_episode"]

                    user_series = UserSeries.objects.filter(
                        user=user,
                        series=series,
                        watched_season=watched_season
                    )
                    if user_series.exists():
                        results.append(cls.update_user_series(
                            user_series=user_series.get(),
                            last_watched_episode=last_watched_episode,
                            request_data=request_data
                        ))
                    else:
                        results.append(cls.create_user_series(
                            user=user,
                            series=series,
                            watched_season=watched_season,
                            last_watched_episode=last_watched_episode,
                            request_data=request_data,
                        ))
            else:
                # Only creates one for given season
                watched_season = seasons.get(season=str(request_data["watched_season"]))
                last_watched_episode = request_data["last_watched_episode"]
                user_series = UserSeries.objects.filter(
                    user=user,
                    series=series,
                    watched_season=watched_season
                )
                if user_series.exists():
                    results.append(cls.update_user_series(
                        user_series=user_series.get(),
                        last_watched_episode=last_watched_episode,
                        request_data=request_data
                    ))
                else:
                    results.append(cls.create_user_series(
                        user=user,
                        series=series,
                        watched_season=watched_season,
                        last_watched_episode=last_watched_episode,
                        request_data=request_data,
                    ))

            return results
        else:
            raise SeriesNotFoundError(f"Series not exists with {request_data['tvfy_code']} tvfy_code.")

    @classmethod
    def get_user_series(cls, user: Account) -> list[dict[str, Any]]:
        query = UserSeries.objects.select_related(
            "series",
            "watched_season",
        ).prefetch_related(
            "series__country",
            "series__genres",
            "series__language",
            "watched_season__episode_set",
        ).filter(user=user)

        watched_user_series_query = query.filter(is_watched=True)
        grouped_series = defaultdict(list)
        for watched_user_series in watched_user_series_query:
            grouped_series[watched_user_series.series].append(watched_user_series.watched_season)

        result = []
        for series, watched_season_list in grouped_series.items():
            last_watched_episode = watched_user_series_query.filter(
                series=series
            ).order_by("-watched_season__season").first().last_watched_episode
            result.append({
                "last_watched_episode": last_watched_episode,
                "series": series,
                "watched_seasons": watched_season_list,
                "unwatched_seasons": list(set(series.season_set.all()) - set(watched_season_list)),
            })

        return result
