var showText = function (target, message, index, interval) {
  if (index < message.length) {
      if(message[index]=='.'){
           $(target).append(message[index++]);
             $(target).append('<br/>');
             $(target).append('<br/>');
        
      }
      else {
          $(target).append(message[index++]);
      }
    setTimeout(function () { showText(target, message, index, interval); }, interval);
  }
}

$(function () {
  var x = "Checks your document against thousands of documents in our database.\
      Supports multiple formats like docx,pdf,doc,txt.\
      Generates bar graph displaying amount of plagiarism among different documents."
  showText("#msg",x, 0, 90);


});



function  popup() {
    document.getElementById("overlay").style.display='inline';
     document.getElementById("overlayWindow").style.display='block';

}

function closepopup(){
    document.getElementById("overlay").style.display='none';
}

function displaysignin(){
    document.getElementById("overlayWindow").style.display='none';
    document.getElementById("overlayWindow1").style.display='block';



}

function back(){
    document.getElementById("overlayWindow").style.display='block';
    document.getElementById("overlayWindow1").style.display='none';
    


}

