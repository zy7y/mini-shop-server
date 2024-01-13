import os
import re
import subprocess

import requests


def update_readme():
    # 获取环境变量
    repo = os.environ.get("REPO_NAME")
    readme_path = os.environ.get("README_PATH")

    # 获取贡献者信息和头像 URL
    response = requests.get(f"https://api.github.com/repos/{repo}/contributors")
    contributors_data = response.json()

    contributors_md = ""
    for contributor in contributors_data:
        if contributor["type"] != "User":
            continue
        login = contributor["login"]
        avatar_url = contributor["avatar_url"]
        html_url = contributor["html_url"]
        contributions = contributor["contributions"]
        contributor_md = f"""
<div style="display: inline-block; text-align: center; margin: 10px;">
    <a href="{html_url}" target="_blank">
        <img src="{avatar_url}" width="100px" height="100px" style="border-radius: 50%;" alt="{login}">
    </a>
    <br>{login}<br>Contributions: {contributions}
</div>
        """
        contributors_md += contributor_md

    # 更新 README 文件
    with open(readme_path, "r") as f:
        readme_content = f.read()

    # 定义要进行匹配和替换的正则表达式模式，使用括号分组
    pattern = re.compile(
        r"<!-- CONTRIBUTORS_SECTION -->.*<!-- /CONTRIBUTORS_SECTION -->", re.DOTALL
    )

    # 定义要替换的字符串
    replacement = f"""
<!-- CONTRIBUTORS_SECTION -->
<div align="center">
    {contributors_md}
</div>
<!-- /CONTRIBUTORS_SECTION -->
    """

    # 使用正则表达式进行匹配和替换
    new_readme_content = pattern.sub(replacement, readme_content)

    # 替换Star History
    star_pattern = re.compile(
        r"<!-- STAR_HISTORY -->.*<!-- /STAR_HISTORY -->", re.DOTALL
    )
    star_replacement = f"""
<!-- STAR_HISTORY -->
[![Star History Chart](https://api.star-history.com/svg?repos={repo}&type=Date)](https://star-history.com/#{repo}&Date)
<!-- /STAR_HISTORY -->
    """
    new_readme_content = star_pattern.sub(star_replacement, new_readme_content)

    # 提交更改
    if new_readme_content != readme_content:
        with open(readme_path, "w") as f:
            f.write(new_readme_content)

        commit_message = f"CI: Update README (contributors: {len(contributors_data)})"
        subprocess.Popen(["git", "add", readme_path])
        subprocess.Popen(["git", "commit", "-m", commit_message])
        subprocess.Popen(["git", "push"])
    else:
        print("no change")


# 在需要的时候调用函数来更新 README
update_readme()
