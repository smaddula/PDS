$( document ).ready(function() {
   

  
    $("#userfile").change(function(){
      readURL(this);
      var url = "/uploadfile"
      var file = $("#userfile")[0].files[0];
      var formdata = new FormData();
      formdata.append("file", file);
      $.ajax({
        url: url,
        data: formdata,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data) {
          $("#uploadform").toggle();
          
          console.log("upload successfull"+data.filename); 
          loadImage('https://s3-us-west-2.amazonaws.com/pdsoxfordimages/'+$.trim(data.filename)+'.jpg', 300, 300, '#result');
        }
      });
    });   

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            
            reader.onload = function (e) {
               $('#inputimage').toggle();
                $('#inputimage').attr('src', e.target.result);
            }
            
            reader.readAsDataURL(input.files[0]);
        }
    }
  
  });


  
  function sendFileToServer(formData,status,url,ug)
  {
      var uploadURL =url; //Upload URL
      var extraData ={}; //Extra Data.
      var jqXHR=$.ajax({
        
        url: uploadURL,
        type: "POST",
        contentType:false,
        processData: false,
        cache: false,
        data: formData,
        success: function(data){
          status.setProgress(100);
          console.log("upload successfull"+data.filename);
        }
      }); 

  status.setAbort(jqXHR);
}

function loadImage(path, width, height, target) {
    $('<img src="'+ path +'">').load(function() {
      $(this).width(width).height(height).appendTo(target);
    });
}

var rowCount=0;
function createStatusbar(obj)
{
 rowCount++;
 var row="odd";
 if(rowCount %2 ==0) row ="even";
 this.statusbar = $("<div class='statusbar "+row+"'></div>");
 this.filename = $("<div class='filename'></div>").appendTo(this.statusbar);
 this.size = $("<div class='filesize'></div>").appendTo(this.statusbar);
 this.progressBar = $("<div class='progressBar'><div></div></div>").appendTo(this.statusbar);
 this.abort = $("<div class='abort'>Abort</div>").appendTo(this.statusbar);
 obj.after(this.statusbar);

 this.setFileNameSize = function(name,size)
 {
  var sizeStr="";
  var sizeKB = size/1024;
  if(parseInt(sizeKB) > 1024)
  {
    var sizeMB = sizeKB/1024;
    sizeStr = sizeMB.toFixed(2)+" MB";
  }
  else
  {
    sizeStr = sizeKB.toFixed(2)+" KB";
  }

  this.filename.html(name);
  this.size.html(sizeStr);
}
this.setProgress = function(progress)
{       
  var progressBarWidth =progress*this.progressBar.width()/ 100;  
  this.progressBar.find('div').animate({ width: progressBarWidth }, 10).html(progress + "% ");
  if(parseInt(progress) >= 100)
  {
    this.abort.hide();
  }
}
this.setAbort = function(jqxhr)
{
  var sb = this.statusbar;
  this.abort.click(function()
  {
    jqxhr.abort();
    sb.hide();
  });
}
}
function handleFileUpload(files,obj,url,ug)
{
 for (var i = 0; i < files.length; i++) 
 {
  var fd = new FormData();
  fd.append('file', files[i]);

          var status = new createStatusbar(obj); //Using this we can set progress.
          status.setFileNameSize(files[i].name,files[i].size);
          sendFileToServer(fd,status,url,ug);

        }
      }
      $(document).ready(function()
      {
        var obj = $("#userdragandrophandler");

        obj.on('dragenter', function (e) 
        {
          e.stopPropagation();
          e.preventDefault();
          $(this).css('border', '2px solid #0B85A1');
        });
        
        obj.on('dragover', function (e) 
        {
         e.stopPropagation();
         e.preventDefault();
       });
        
        obj.on('drop', function (e) 
        {

         $(this).css('border', '2px dotted #0B85A1');
         e.preventDefault();
         var files = e.originalEvent.dataTransfer.files;

       //We need to send dropped files to Server
       handleFileUpload(files,obj,"/uploadfile","user");
     });
        
        $(document).on('dragenter', function (e) 
        {
          e.stopPropagation();
          e.preventDefault();
        });
        $(document).on('dragover', function (e) 
        {
          e.stopPropagation();
          e.preventDefault();
          obj.css('border', '2px dotted #0B85A1');
        });
        $(document).on('drop', function (e) 
        {
          e.stopPropagation();
          e.preventDefault();
        });

      });
