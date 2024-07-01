//for Create Account page





//for Dashboard Page

function uploadfile(obj){

  obj.style.display='none';
  document.getElementById('fileInput').style.display='block';
  document.getElementById('uploadBtn').style.display='block';

}

const elmnt = document.querySelector(".ExactElement");
elmnt.addEventListener("contextmenu", function(e){
  e.preventDefault();

});



function DeleteFile(obj){   //add element to argomans and replace with 0

  if(1){   //if user is owner
    obj[0].remove();
  }
  
}