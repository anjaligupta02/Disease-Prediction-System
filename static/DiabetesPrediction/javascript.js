<script>
  /* When the user clicks on the button,
toggle between hiding and showing the dropdown content */


function Functionshow() {
  document.getElementById("searchbar").value = '';
  document.getElementById("myDropdown").classList.toggle("show");
   search_symptoms();

}


// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.btn')) {
    if (!event.target.matches('.searchbardiv')){
      if (!event.target.matches('.searchbar')){

    var dropdowns = document.getElementsByClassName("drop-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {

      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
}
}

  function Functionsymptoms(name) {
    var newItem = document.createElement("TEXTAREA");
    newItem.innerText = name;
    newItem.setAttribute("id","symptoms");

    newItem.setAttribute("class","symptoms");
    document.getElementById("sympbox").appendChild(newItem);

  }


  //var elements = document.getElementsByClassName("symptoms");


  function search_symptoms() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('dropdown-item');

    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="inline-block";
        }
    }
}


$(document).ready( function(){


$("#predict").click(function () {
  event.preventDefault();

  var symptoms = document.getElementsByClassName("symptoms");
  var noofsym = symptoms.length;
  var symlist=[];

  if(noofsym == 0){
     alert(" please add some symptoms ");
  }

  else {

  for(i=0;i<symptoms.length;i++){
    symlist[i]=symptoms[i].value;
  }



  $("#resultdiv").show("slow");
  $('html,body').animate({
    scrollTop: $("#resultdiv").offset().top},
    'slow');




  $.ajax({
      url: 'checkdisease',
      type: "POST",
      data: { "noofsym" : noofsym,
              "symptoms" :symlist,
              csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val()
      },
      dataType: 'json',


    });
  }
  });
});

</script>
