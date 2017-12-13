$('#delivery_rejection_modal').on('show.bs.modal', function(event) {

	var button = $(event.relatedTarget)
	var itempk = button.data('itempk')

	var modal = $(this)
	modal.find('.modal-content').attr("id", "delivery_rejection_modal_" + itempk)
	modal.find('.modal-body form').attr("action", "/reject_delivery/" + itempk +"/")
	modal.find('.modal-footer button').attr("id", "close_modal_" + itempk)
})