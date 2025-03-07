---
title: My Fist Test Post
search: true
categories:
    - test-pages
tags:
    - test
---

This post should not appear in the search index because it has the following YAML Front Matter:

```yaml
search: false
```

<video id="myVideo" src="assets/videos/LightEndoStereo_demo.mp4" controls></video>
<button onclick="playVideo()">Play</button>
<button onclick="pauseVideo()">Pause</button>
<script>
  function playVideo() {
    document.getElementById('myVideo').play();
  }
  function pauseVideo() {
    document.getElementById('myVideo').pause();
  }
</script>