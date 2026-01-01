---
layout: about
title: About
permalink: /
# subtitle: <a href='#'>A Ph.D. candidate at Shanghai Jiao Tong University</a>.

profile:
  align: left
  image: prof_pic.png
  image_circular: false # crops the image to make it circular
  more_info:
    # <p> 🚩 Xuhui, Shanghai, China </p>

selected_papers: true # includes a list of papers marked as "selected={true}"
social: false # includes social icons at the bottom of the page

announcements:
  enabled: false # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: true
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts

# Page-level performance toggles
badges: false
math: false
---

<!-- 整合的个人信息卡片 -->
<div class="cv-basics-box">
  <div class="card-header">
    <div class="basics-title"><b>Information</b></div>
    <div class="intro-text">Hi, I am 丁阳 (Yang Ding, or Sunny), now a Ph.D. candidate.</div>
  </div>

  <div class="card-content">
    <div class="profile-image-container">
      <!-- Profile image will be moved here by JavaScript -->
    </div>
    
    <div class="basics-item">
      <span>
        <span class="key"><b>👨‍🏫 My Advisor</b></span>
        <span class="colon">:</span>
        <span class="value"><a href="https://imr.sjtu.edu.cn/sz_teachers/3023.html">Prof. Dahong Qian</a></span>
      </span>

      <span>
        <span class="key"><b>📬 Email</b></span>
        <span class="colon">:</span>
        <span class="value"><a href="mailto:yang_ding@sjtu.edu.cn">yang_ding@sjtu.edu.cn</a></span>
      </span>

      <span>
        <span class="key"><b>🏛 Affiliation</b></span>
        <span class="colon">:</span>
        <span class="value">Shanghai Jiao Tong University</span>
      </span>

      <span>
        <span class="key"><b>💡 Interests</b></span>
        <span class="colon">:</span>
        <span class="value">Endoscopic Image Processing, Stereo Matching, 3D Reconstruction</span>
      </span>
    </div>

  </div>
</div>

<!-- 日期进度条卡片 -->
<div class="cv-basics-box progress-timeline-box" style="margin-top: 2rem;">
  <div class="card-header">
    <div class="basics-title progress-timeline-title"><b>Progress Timeline</b></div>
    <div class="intro-text"><span id="progress-days-passed-header">0</span> / <span id="progress-total-days-header">731</span> days</div>
  </div>

  <div class="card-content">
    <div class="progress-timeline-container">
      <div id="progress-timeline" class="progress-timeline"></div>
    </div>
  </div>
</div>

<style>
.progress-timeline-box .progress-timeline-title {
  font-size: 1.3rem !important;
}

.progress-timeline-container {
  width: 100%;
  padding: 1rem 0;
}

.progress-timeline {
  display: flex;
  flex-wrap: wrap;
  gap: 3px;
  justify-content: flex-start;
  margin-bottom: 1rem;
}

.progress-day {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  background-color: #ebedf0;
  border: 1px solid #d1d5da;
  transition: all 0.2s ease;
}

.progress-day.passed {
  background-color: #40c463;
  border-color: #40c463;
}

.progress-day:hover {
  transform: scale(1.2);
  z-index: 1;
  position: relative;
}


@media (max-width: 768px) {
  .progress-timeline {
    gap: 2px;
  }
  
  .progress-day {
    width: 10px;
    height: 10px;
  }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  // Move profile image to the new location inside the card
  const originalProfile = document.querySelector('.post .profile');
  const profileImageContainer = document.querySelector('.profile-image-container');
  
  if (originalProfile && profileImageContainer) {
    // Clone the profile content
    const profileClone = originalProfile.cloneNode(true);
    profileClone.classList.add('relocated-profile');
    profileClone.style.opacity = '1';
    profileClone.style.position = 'static';
    profileClone.style.pointerEvents = 'auto';
    // Add to new location inside the card
    profileImageContainer.appendChild(profileClone);
  }

  // Initialize progress timeline
  function initProgressTimeline() {
    const startDate = new Date('2026-01-01');
    const endDate = new Date('2028-01-01');
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Reset time to start of day
    
    const timelineContainer = document.getElementById('progress-timeline');
    const daysPassedHeaderSpan = document.getElementById('progress-days-passed-header');
    const totalDaysHeaderSpan = document.getElementById('progress-total-days-header');
    
    if (!timelineContainer) return;
    
    // Calculate total days
    const totalDays = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));
    if (totalDaysHeaderSpan) {
      totalDaysHeaderSpan.textContent = totalDays;
    }
    
    // Clear existing content
    timelineContainer.innerHTML = '';
    
    let daysPassed = 0;
    
    // Generate day blocks
    for (let i = 0; i < totalDays; i++) {
      const currentDate = new Date(startDate);
      currentDate.setDate(startDate.getDate() + i);
      
      const dayBlock = document.createElement('div');
      dayBlock.className = 'progress-day';
      dayBlock.setAttribute('data-date', currentDate.toISOString().split('T')[0]);
      
      // Check if this day has passed
      if (currentDate < today) {
        dayBlock.classList.add('passed');
        daysPassed++;
      }
      
      // Add tooltip on hover
      dayBlock.title = currentDate.toISOString().split('T')[0];
      
      timelineContainer.appendChild(dayBlock);
    }
    
    // Update days passed counter in header
    if (daysPassedHeaderSpan) {
      daysPassedHeaderSpan.textContent = daysPassed;
    }
  }
  
  // Initialize the timeline
  initProgressTimeline();
});
</script>
