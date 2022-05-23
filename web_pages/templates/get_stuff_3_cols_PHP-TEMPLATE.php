<?php
    $title = "The Design-O-Matic - Auto-Generated T-Shirt Designs Using Python and Gimp, Auto-Uploaded to Amazon Merch";
    $keywords = "python, amazon, merch, tshirts, t-shirts, t shirts, designs, parody, cat, gorilla, ape, jvzdesigns, programming, script, github, automation, redbubble, teepublic, pod, print on demand, gimp, gimp fu, python fu, cartoon, funny, design-o-matic, design o matic";
    $description = "Python project to automate the process of uploading designs to Amazon Merch, then creates web pages, including this one, linking to the specific Amazon Merch page for each design.";

    include('../header.php');
?>

<body>
<button onclick="topFunction()" id="myBtn" title="Go to top">Back To Top</button>

        <div id="youtube">

        <iframe width="560" height="315" src="https://www.youtube.com/embed/sq1aM_eeNy4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

        </div>

    <div class="row">
        
        <div class="column">

            {% for value in column1 %}
            <a href = "http://www.jvzdesigns.com/get-stuff/{{value[:-4]}}.html"><img src="http://www.jvzdesigns.com/get-stuff/get-thumbs/{{value}}" alt = "{{value[0:3]}} {{value[4:-4]}}" /></a>
            {% endfor %}

        </div>

        <div class="column">

            {% for value in column2 %}
            <a href = "http://www.jvzdesigns.com/get-stuff/{{value[:-4]}}.html"><img src="http://www.jvzdesigns.com/get-stuff/get-thumbs/{{value}}" alt = "{{value[0:3]}} {{value[4:-4]}}" /></a>
            {% endfor %}

        </div>

        
        <div class="column">

            {% for value in column3 %}
            <a href = "http://www.jvzdesigns.com/get-stuff/{{value[:-4]}}.html"><img src="http://www.jvzdesigns.com/get-stuff/get-thumbs/{{value}}" alt = "{{value[0:3]}} {{value[4:-4]}}" /></a>
            {% endfor %}            

        </div>
            
    
    </div>

<!-- BACK TO TOP SCRIPT -->

<script> 
//Get the button:
mybutton = document.getElementById("myBtn");

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

<?php include '../footer.php' ?>
</body>
</html>