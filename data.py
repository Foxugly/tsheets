from customusers.models import CustomUser
from projects.models import Project
from categories.models import Category
from projectcategories.models import ProjectCategory
from datetime import datetime, timedelta
from weeks.models import Week, WeekDate
from teams.models import Team

team = Team.objects.create(name="Fedasil")
team.save()

dict_users = [{'name': "Renaud", 'last_name': "Vilain", 'superuser': True, 'teamleader': True},
              {'name': "Olivier", 'last_name': "Gevers", 'superuser': False, 'teamleader': True},
              {'name': "Thomas", 'last_name': "Dawance", 'superuser': False, 'teamleader': True},
              {'name': "Pierre", 'last_name': "Binet", 'superuser': False, 'teamleader': False},
              {'name': "Paul", 'last_name': "Mirabelle", 'superuser': False, 'teamleader': False}, ]
for dict_user in dict_users:
    u = CustomUser.objects.create_user(dict_user['name'], password=dict_user['name'], current_team=team,
                                       first_name=dict_user['name'], last_name=dict_user["last_name"])
    u.is_superuser = dict_user['superuser']
    u.save()
    if dict_user['teamleader']:
        team.teamleaders.add(u)
    else:
        team.members.add(u)

    print("create customuser : ", u)

user = CustomUser.objects.get(username="Renaud")

# create categories
categories_project = ["Analyse", "Developpement", "Meetings"]
for cat in categories_project:
    c = Category(name=cat, to_projects=True, to_admin=False)
    c.save()
    print("create category : ", c)

categories_adm = ["Holiday", "Sick", ]
for cat in categories_adm:
    c = Category(name=cat, to_projects=False, to_admin=True)
    c.save()
    print("create category : ", c)

# create projects
projects = ["MatchIT 6.4", "MatchIT 6.5"]
for project in projects:
    p = Project(name=project, refer_team=team)
    p.save()
    team.projects.add(p)

projects = ["MatchIT Administratif", ]
for project in projects:
    p = Project(name=project, refer_team=team, project=False, admin=True)
    p.save()
    team.projects.add(p)

for user in CustomUser.objects.all():
    for pc in ProjectCategory.objects.all():
        user.categories.add(pc)
        print("link : ", user, "===", pc)

now = datetime.now()
week = int(now.isocalendar().week)
year = int(now.year)
monday = datetime.strptime(str(year) + "-W" + str(week) + '-1', "%Y-W%W-%w")

for i in range(5):
    future = monday + timedelta(days=i * 7)
    wd = WeekDate(week=future.isocalendar().week, year=future.isocalendar().year, start_date=future,
                  end_date=future + timedelta(days=6), )
    wd.save()
    print(wd)
    for user in CustomUser.objects.all():
        w = Week.objects.create(weekdate=wd, refer_user=user, refer_team=team)
        w.save()
        print(user)
