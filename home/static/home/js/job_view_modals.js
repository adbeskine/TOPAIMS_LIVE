$('#purchase_order_modal').on('show.bs.modal', function(event) {

	var button = $(event.relatedTarget)
	var pk = button.data('pk')
	var quantity = button.data('quantity')
	var job = button.data('job')
	var jobid =  button.data('jobid')
	var model = button.data('model')
	var description = button.data('description')

	var modal = $(this)
	modal.find('.modal-content').attr("id", "purchase_order_modal_" + pk)
	modal.find('.modal-body form').attr("action", "/purchase_order/" + jobid + "/")
	modal.find('.modal-body form').attr("id", "PO_form_" + model + "_" + pk)

	modal.find('.item_1_description').attr("value", description)
	modal.find('.item_1_job').attr("value", job)
	modal.find('.item_1_quantity').attr("value", quantity)

})

$('#date_form_modal').on('show.bs.modal', function(event) {

	var button = $(event.relatedTarget)
	var pk = button.data('pk')
	var description = button.data('desc')
	var quantity = button.data('quantity')
	var job = button.data('job')

	var modal = $(this)
	modal.find('.modal-content').attr("id", "date_form_modal_" + pk)

	modal.find('.update_date_form').attr("action", "/schedule_item/update/" + pk +"/")

	modal.find('.delete_form').attr("action", "/schedule_item/delete/" + pk +"/")
	modal.find('.delete_form_submit').attr("value", "Delete " + description)

	modal.find('.shopping_list_form').attr("action", "/shopping_list/create/")
	modal.find('.SL_desc').attr("value", description)
	modal.find('.SL_q').attr("value", quantity)
	modal.find('.SL_job').attr("value", job)


})