<div class="jvz-gs-link">

{% for key, value in last_page.items() %}

<a href = "{{value}}"><img src="http://www.jvzdesigns.com/get-stuff/get-thumbs/{{key}}" alt = "{{key[0:3]}} {{key[4:-4]}}" /></a>

{% endfor %}

</div>

<!-- status elements for infinite scroll -->
<div class="scroller-status">
    <div class="infinite-scroll-request loader-ellips">
      ...
    </div>
    <p class="infinite-scroll-last">End of content</p>
    <p class="infinite-scroll-error">No more pages to load</p>
  </div>