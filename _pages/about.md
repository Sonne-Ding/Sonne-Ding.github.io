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
  enabled: true # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: true
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

<!-- 整合的个人信息卡片 -->
<div class="cv-basics-box">
  <div class="card-header">
    <div class="basics-title"><b>Information</b></div>
    <div class="intro-text">Hi, I am 丁阳 (Yang Ding, or Sunny Ding), now a Ph.D. candidate.</div>
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
});
</script>
