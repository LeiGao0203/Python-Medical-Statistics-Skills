#!/usr/bin/env bash
set -eu

repo_root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
tmp_dir="$(mktemp -d)"

cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

assert_dir() {
  if [ ! -d "$1" ]; then
    printf 'Expected directory missing: %s\n' "$1" >&2
    exit 1
  fi
}

assert_file() {
  if [ ! -f "$1" ]; then
    printf 'Expected file missing: %s\n' "$1" >&2
    exit 1
  fi
}

target_local="$tmp_dir/local-skills"
AGENT_SKILLS_DIR="$target_local" bash "$repo_root/install.sh"

for skill in \
  ttest anova chisq correlation nonparametric roc sample-size \
  logistic-reg multi-reg survival pca ps-matching subgroup-analysis \
  python-script jupyter-notebook
do
  assert_dir "$target_local/$skill"
  assert_file "$target_local/$skill/SKILL.md"
done

source_target="$tmp_dir/source-skills"
RUNTIME_SOURCE="$repo_root" AGENT_SKILLS_DIR="$source_target" PY_MED_STATS_SOURCE="$repo_root" bash "$repo_root/install.sh"

assert_file "$source_target/ttest/SKILL.md"
assert_file "$source_target/jupyter-notebook/SKILL.md"

archive_root="$tmp_dir/archive-root"
archive_source="$archive_root/Python-Medical-Statistics-Skills-main"
mkdir -p "$archive_source"
cp -R "$repo_root"/advanced-stats "$archive_source"/
cp -R "$repo_root"/basic-stats "$archive_source"/
cp -R "$repo_root"/literature-stats "$archive_source"/
cp -R "$repo_root"/python-script "$archive_source"/
cp -R "$repo_root"/jupyter-notebook "$archive_source"/

archive_file="$tmp_dir/source.tar.gz"
(cd "$archive_root" && tar -czf "$archive_file" Python-Medical-Statistics-Skills-main)

archive_target="$tmp_dir/archive-skills"
PY_MED_STATS_ARCHIVE_URL="file://$archive_file" AGENT_SKILLS_DIR="$archive_target" bash "$repo_root/install.sh"

assert_file "$archive_target/logistic-reg/SKILL.md"
assert_file "$archive_target/python-script/SKILL.md"

printf 'install_test.sh passed\n'
