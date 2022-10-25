$(document).ready(function(){
	$(".btnlogout").click(function(){
		conmsg=confirm("Do you want to logout ?")
		if(conmsg==1){
			window.location.href="/logout"
		}
	})
	$(".btnaddproject").click(function(){
		$(".maincontainer").load("/addproject")
	})
	$(".btnviewprojects").click(function(){
		$(".maincontainer").load("/viewprojects")
	})
	$(".btnaddblog").click(function(){
		$(".maincontainer").load("/addblog")
	})
	
})