//for Create Account page
const signUpForm = document.getElementById('signupForm');
const messageDiv = document.getElementById('message');

signUpForm.addEventListener('submit', function(event) {
  event.preventDefault();

  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  const confpassDiv = document.getElementById("confpassDiv");

  if (password !== confirmPassword) {
    messageDiv.innerText = "Passwords do not match!";
    messageDiv.style.color = 'red';
    confpassDiv.style.border='1px solid red';
  } 
  else {
    // go to Vrify Account    

    window.location.href = 'VerifySent.html';
    
  }
});


//for Dashboard Page

function uploadfile(obj){

  obj.style.display='none';
  document.getElementById('fileInput').style.display='block';
  document.getElementById('uploadBtn').style.display='block';

}

function OwnerPop(obj , share , del){    //add element to argomans and replace with 0

  const elem = document.getElementsByClassName('ExactElement');
  elem[0].style.zIndex='9';

  if(1){    //if user is owner

    if( obj[0].style.display == 'none'){
      obj[0].style.display='block';
    }
    
    else{
      obj[0].style.display='none';
    } 
  }

  else{    //user is not owner

    if( obj[0].style.display == 'none'){
      obj[0].style.display='block';
    }
    
    else{
      obj[0].style.display='none';
    } 

    share[0].remove();
    del[0].remove();

  }

}


const elmnt = document.getElementById("ExactElement");
elmnt.addEventListener("contextmenu", function(e){
  e.preventDefault();
  
  //show Owner Popup

});



function DeleteFile(obj){   //add element to argomans and replace with 0

  if(1){   //if user is owner
    obj[0].remove();
  }
  
}


function toggleSvgDisplay() {  //it is just for the first person; for all people, it depends on the number of near people
  const checkbox = document.getElementById("myCheckbox");

  const svg = document.getElementById("mySvg");
  const newSvg = document.createElement("div");
  const parent = document.getElementById("parent");
  const pparent = document.getElementById("pparent");
  const child = document.getElementById("selected");
  newSvg.innerHTML = svg.innerHTML;

  if (checkbox.checked) {

    parent.replaceChild(newSvg, child);
    checkbox.addEventListener('change', toggleSvgDisplay());
  } 
  else  {
    
    parent.remove();
    const newparent = document.createElement("div");
    newparent.innerHTML = `<div  id="parent" style="margin-left: 1vw;" ><div id="selected" ></div></div>`;
    pparent.appendChild(newparent);

  }
}
