---
layout: page
permalink: /repositories/
title: Repositories
description:
nav: true
nav_order: 4
---

{% if site.data.repositories.github_users %}

## GitHub Statistics

<div class="container">
  {% for user in site.data.repositories.github_users %}
  
  <!-- GitHub Streak -->
  <div class="row mb-4">
    <div class="col-12">
      <div class="text-center">
        {% include repository/repo_streak.liquid %}
      </div>
    </div>
  </div>
  
  <!-- Activity Chart Row -->
  <div class="row mb-4">
    <div class="col-12">
      <div class="card repo-card activity-card">
        <div class="card-body text-center">
          <h5 class="card-title">Activity Overview</h5>
          {% include repository/repo_activity.liquid username=user %}
        </div>
      </div>
    </div>
  </div>
  
  {% endfor %}
</div>

{% comment %}
{% if site.repo_trophies.enabled %}
{% for user in site.data.repositories.github_users %}
{% if site.data.repositories.github_users.size > 1 %}

<h4>{{ user }}</h4>
{% endif %}
<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
{% include repository/repo_trophies.liquid username=user %}
</div>
---
{% endfor %}
{% endif %}
{% endcomment %}

{% endif %}

{% if site.data.repositories.github_repos %}

## Public Repositories

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.liquid repository=repo %}
  {% endfor %}
</div>
{% endif %}
