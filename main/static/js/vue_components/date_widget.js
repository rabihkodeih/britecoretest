Vue.component("date_widget", {
	template: '<input class="form-control" type="text"/>',
	mounted: function() {
		$(this.$el).datepicker();
	},
	beforeDestroy: function() {
	    $(this.$el).datepicker('destroy');
	},
})
