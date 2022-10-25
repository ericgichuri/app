$(document).ready(function(){
	$(".formaddblog").on("submit",function(e){
		e.preventDefault()
		var blogdata=new FormData(this)
		$.ajax({
			url: "/addblog",
			method:"post",
			data: blogdata,
			contentType:false,
			processData:false,
			success:function(response){
				if(response.message==1){
					alert("blog posted successfully")
					$(".formaddblog")[0].reset()
					$(".img1hol img").attr("src","")
					$(".blogsubcategory").empty()
					$(".blogsubcategory").append("<option value=''>Select category</option>")
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
	$(".btn-cancel").click(function(){
		$(".img1hol img").attr("src","")
		$(".blogsubcategory").empty()
		$(".blogsubcategory").append("<option value=''>Select category</option>")
	})
	$(".blogcategory").change(function(){
		var category=$(this).val()
		if(category=="Programming"){
			$(".blogsubcategory").empty()
			$(".blogsubcategory").append("<option>Web Development</option>")
			$(".blogsubcategory").append("<option>Web Design</option>")
			$(".blogsubcategory").append("<option>Android dev</option>")
			$(".blogsubcategory").append("<option>Desktop dev</option>")
			$(".blogsubcategory").append("<option>Artifical intelligence</option>")
			$(".blogsubcategory").append("<option>Machine learning</option>")
		}else if(category=="Softwares"){
			$(".blogsubcategory").empty()
			$(".blogsubcategory").append("<option>Desktop Apps</option>")
			$(".blogsubcategory").append("<option>Android Apps</option>")
			$(".blogsubcategory").append("<option>IOS Apps</option>")
		}else if(category=="Computers"){
			$(".blogsubcategory").empty()
			$(".blogsubcategory").append("<option>Desktops</option>")
			$(".blogsubcategory").append("<option>Laptops</option>")
		}else if(category=="Phone"){
			$(".blogsubcategory").empty()
			$(".blogsubcategory").append("<option>Tecno</option>")
			$(".blogsubcategory").append("<option>Samsung</option>")
			$(".blogsubcategory").append("<option>Itel</option>")
			$(".blogsubcategory").append("<option>Iphones</option>")
			$(".blogsubcategory").append("<option>Huawei</option>")
			$(".blogsubcategory").append("<option>Oppo</option>")
		}else if (category=="Motivations"){
			$(".blogsubcategory").empty()
			$(".blogsubcategory").append("<option>Life</option>")
			$(".blogsubcategory").append("<option>Happy</option>")
			$(".blogsubcategory").append("<option>Bible</option>")
			$(".blogsubcategory").append("<option>Success</option>")
		}else{
			$(".blogsubcategory").empty()
			$(".blogsubcategory").append("<option value=''>Select category</option>")
		}
	})
})