$(document).ready(function(){
	
	$(".formaddproject").on("submit",function(e){
		e.preventDefault()
		var projectdata=new FormData(this)
		projectdata.append('img1',$('.uploadimg1').prop('files')[0])
		$.ajax({
			url: "/uploadproject",
			method:"post",
			data: projectdata,
			contentType:false,
			processData:false,
			success:function(response){
				if(response.message==1){
					alert("Project posted successfully")
					$(".formaddproject")[0].reset()
					$(".img1hol img").attr("src","")
					$(".img2hol img").attr("src","")
				}
				else{
					alert(response.message)
				}
			}
		})
	})
	$(function(){
		$(".uploadimg1").change(function(event){
			var file=URL.createObjectURL(event.target.files[0])
			$(".img1hol img").attr("src",file)
		})
	})
	$(function(){
		$(".uploadimg2").change(function(event){
			var file=URL.createObjectURL(event.target.files[0])
			$(".img2hol img").attr("src",file)
		})
	})
	$(".btn-cancel").click(function(){
		$(".img1hol img").attr("src","")
		$(".img2hol img").attr("src","")
	})
})