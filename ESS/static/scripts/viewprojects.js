$(document).ready(function(){
	$(".btnedit").click('button[data-role=edit]',function(){
		var id=$(this).data("id")
		var title=$('#'+id).children('td[data-target=title]').text()
		var briefinfo=$('#'+id).children('td[data-target=briefinfo]').text()
		var description=$('#'+id).children('td[data-target=description]').text()
		var dateposted=$('#'+id).children('td[data-target=dateposted]').text()
		var link=$('#'+id).children('td[data-target=link]').text()
		var status=$('#'+id).children('td[data-target=status]').text()

		$("#eprojecttitle").val(title)
		$("#ebriefinfo").val(briefinfo)
		$("#eprojectdescription").val(description)
		$("#edateposted").val(dateposted)
		$("#eprojectlink").val(link)
		$("#eprojectstatus").val(status)
		$("#my-modal").show()
	})
	$(".btnclosemodal").click(function(){
		$("#my-modal").hide()
	})
})