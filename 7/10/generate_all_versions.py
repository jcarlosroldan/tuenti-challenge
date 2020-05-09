from dateutil.parser import parse
from json import dump
from os import chdir
from subprocess import check_output

def group_list(l, each):
	i = 0
	res = []
	while i < len(l):
		res.append(l[i:i+each])
		i += each
	return res

chdir("repo")
changes_dict = {}

# -----------------------------------------------------------------------------

check_output("git config core.autocrlf false")

# add all regular versions
all_commits = [l.strip().split("\n") for l in check_output("git log --all --branches script.php").decode().strip().split("commit")[1:]]
for commit_id, author, date, _, msg in all_commits:
	diff = check_output("git diff %s" % commit_id)
	if len(diff) > 69:
		ls = diff.decode().split("\n")
		date = parse(date[5:]).strftime("%F")
		changes_dict[date] = [
			int(ls[10].split(" = ")[1][:-1]),
			int(ls[11].split(" = ")[1][:-1])
		]

# add latest version
changes_dict['2017-01-31'] = [
	int(ls[12].split(" = ")[1][:-1]),
	int(ls[13].split(" = ")[1][:-1])
]

# add unreachable childs
all_unreachable = [l.split(" ")[-1] for l in check_output("git fsck --unreachable").decode().split("\n") if "commit" in l]
for commit_id in all_unreachable:
	diff = check_output("git show %s" % commit_id).decode().split("\n")
	date = parse(diff[2][5:]).strftime("%F")
	changes_dict[date] = [
		int(diff[16].split(" = ")[1][:-1]),
		int(diff[17].split(" = ")[1][:-1])
	]


# add dangling
all_dangling = [l.split(" ")[-1] for l in check_output("git fsck --full").decode().split("\n") if "commit" in l]
for commit_id in all_dangling:
	diff = check_output("git show %s" % commit_id).decode().split("\n")
	date = parse(diff[2][5:]).strftime("%F")
	changes_dict[date] = [
		int(diff[16].split(" = ")[1][:-1]),
		int(diff[17].split(" = ")[1][:-1])
	]

# -----------------------------------------------------------------------------

print(len(changes_dict))
chdir("..")
with open("secrets.json", "w") as f:
	dump(changes_dict, f)