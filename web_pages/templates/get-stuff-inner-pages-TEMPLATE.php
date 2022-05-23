<div class="jvz-gs-link">

{% for key, value in stuff.items() %}

<a href = "{{value}}"><img src="http://www.jvzdesigns.com/get-stuff/get-thumbs/{{key}}" alt = "{{key[0:3]}} {{key[4:-4]}}" /></a>

{% endfor %}

</div>

<div class="scroller-status">
    <div class="loader-ellips infinite-scroll-request">
      <span class="loader-ellips__dot"></span>
      <span class="loader-ellips__dot"></span>
      <span class="loader-ellips__dot"></span>
      <span class="loader-ellips__dot"></span>
    </div>
</div>

<p class="pagination">
    <a class="pagination__next" href="gs-page{{ dict_count + 1 }}.html">Next page</a>
</p>