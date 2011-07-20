$(document).ready(function () {
  $("id_object_id").options.length = 0; //vaciar options
  $("id_object_id").options[0] = new Option("-------"); //vaciar options
  $("id_content_type").change(function () {
    var value = $("id_content_type").value;
    var url  = "/admin/agenda/update/" + value + "/";
    $getJSON.(url, function(data) {
      for(i=0; i<data.length; i++){
        $("id_object_id").options[i+1] = new Option(data[i][1], data[i][0]);
    });
});      
