$('#delivery_rejection_modal').on('show.bs.modal', function(event) {

	var button = $(event.relatedTarget)
	var itempk = button.data('itempk')

	var modal=$(this)
	modal.find('.modal-content').setAttribute("id", "delivery_rejection_modal_" + itempk)
	modal.find('.modal-body form').setAttribute("action", "{% url 'reject delivery' " + itempk + " %}")
	modal.find('.modal-footer button').setAttribute("id", "close_modal_"+itempk)
})