from django.db import models
from multiselectfield import MultiSelectField
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Player(TimeStampedModel):
    class FantasyPosition(models.TextChoices):
        QUARTERBACK = 'QB'
        RUNNING_BACK = 'RB'
        WIDE_RECEIVER = 'WR'
        TIGHT_END = 'TE'
        KICKER = 'K'
        DEFENSE = 'DEF'
        DEFENSIVE_BACK = 'DB'
        LINEBACKER = 'LB'
        DEFENSIVE_LINE = 'DL'
        OFFENSIVE_LINE = 'OL'
        OFFENSIVE_GUARD = 'OG'
        OFFENSIVE_TACKLE = 'OT'
        LONG_SNAPPER = 'LS'
        PUNTER = 'P'

    class TeamChoices(models.TextChoices):
        ARIZONA = 'ARI'
        ATLANTA = 'ATL'
        BALTIMORE = 'BAL'
        BUFFALO = 'BUF'
        CAROLINA = 'CAR'
        CHICAGO = 'CHI'
        CINCINNATI = 'CIN'
        CLEVELAND = 'CLE'
        DALLAS = 'DAL'
        DENVER = 'DEN'
        DETROIT = 'DET'
        GREEN_BAY = 'GB'
        HOUSTON = 'HOU'
        INDIANAPOLIS = 'IND'
        JACKSONVILLE = 'JAX'
        KANSAS_CITY = 'KC'
        LAS_VEGAS = 'LV'
        LOS_ANGELES_RAMS = 'LAR'
        MIAMI = 'MIA'
        MINNESOTA = 'MIN'
        NEW_ENGLAND = 'NE'
        NEW_ORLEANS = 'NO'
        NEW_YORK_GIANTS = 'NYG'
        NEW_YORK_JETS = 'NYJ'
        PHILADELPHIA = 'PHI'
        PITTSBURGH = 'PIT'
        SAN_FRANCISCO = 'SF'
        SEATTLE = 'SEA'
        TAMPA_BAY = 'TB'
        TENNESSEE = 'TEN'
        WASHINGTON = 'WAS'

    player_id = models.CharField(primary_key=True, unique=True, db_index=True, max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    full_name = models.CharField(max_length=250)
    search_full_name = models.CharField(max_length=250)
    search_first_name = models.CharField(max_length=250)
    search_last_name = models.CharField(max_length=250)
    team = models.CharField(choices=TeamChoices.choices, max_length=250, null=True, blank=True)
    position = models.CharField(max_length=250, null=True, blank=True)
    fantasy_positions = MultiSelectField(choices=FantasyPosition.choices, max_length=250, null=True, blank=True)
    years_exp = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=False)
    status = models.CharField(max_length=250, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    depth_chart_position = models.CharField(max_length=250, null=True, blank=True)
    depth_chart_order = models.IntegerField(null=True, blank=True)
    sport = models.CharField(default='nfl', max_length=250)
    search_rank = models.IntegerField(default=9999999, null=True, blank=True)

    def __str__(self):
        return self.search_full_name

class PlayerMetadata(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='metadata')
    # rookie_year = models.CharField(max_length=250, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    height = models.CharField(max_length=250, null=True, blank=True)
    weight = models.CharField(max_length=250, null=True, blank=True)
    college = models.CharField(max_length=250, null=True, blank=True)
    high_school = models.CharField(max_length=250, null=True, blank=True)

class PlayerIDs(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='ids')
    # channel_id = models.CharField(max_length=250, null=True, blank=True)
    fantasy_data_id = models.IntegerField(null=True, blank=True)
    stats_id = models.IntegerField(null=True, blank=True)

# class Injury(models.Model):
#     player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='injuries')
#     body_part = models.CharField(max_length=250, null=True, blank=True)
#     status = models.CharField(max_length=250, null=True, blank=True)
#     notes = models.TextField(null=True, blank=True)
#     start_date = models.DateField(null=True, blank=True)

