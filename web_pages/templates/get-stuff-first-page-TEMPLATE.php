<?php
    $title = "The Design-O-Matic - Auto-Generated T-Shirt Designs Using Python and Gimp, Auto-Uploaded to Amazon Merch";
    $keywords = "python, amazon, merch, tshirts, t-shirts, t shirts, designs, parody, cat, gorilla, ape, jvzdesigns, programming, script, github, automation, redbubble, teepublic, pod, print on demand, gimp, gimp fu, python fu, cartoon, funny, design-o-matic, design o matic";
    $description = "Python project to automate the process of uploading designs to Amazon Merch, then creates web pages, including this one, linking to the specific Amazon Merch page for each design.";

    include('../mobile/mindex-header.php');
?>

<div class="container" data-infinite-scroll='{ "path": ".pagination__next", "append": ".jvz-gs-link", "history": false }'>

<button onclick="topFunction()" id="myMobBtn" title="Go to top">Back To Top</button>

<div id="mob_youtube" style="text-align:center; margin:30px auto 20px auto;">

        <iframe width="280" height="157" src="https://www.youtube.com/embed/sq1aM_eeNy4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

</div>

    <div class="row">
        
        <div class="column">

            <div class="jvz-gs-link">

            {% for key, value in first_page.items() %}

            <a href = "{{value}}"><img src="http://www.jvzdesigns.com/get-stuff/get-thumbs/{{key}}" alt = "{{key[0:3]}} {{key[4:-4]}}" /></a>

            {% endfor %}

            </div>
        </div>
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
        <a class="pagination__next" href="../mobile/get-stuff-pages/gs-page1.html"></a>
      </p>
        
        <script>
    function myFunction() {
      var x = document.getElementById("myLinks");
      if (x.style.display === "block") {
        x.style.display = "none";
      } else {
        x.style.display = "block";
      }
    }
    </script>

<!-- BACK TO TOP SCRIPT -->

<script> 
//Get the button:
mybutton = document.getElementById("myMobBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

</script>

    </div>
</body>
</html>