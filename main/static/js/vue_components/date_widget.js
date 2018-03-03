Vue.component("date_widget", {
	template: '<input class="form-control" type="text"/>',
	props: ['value'],
	mounted: function() {
		let self = this;
		$(this.$el).datepicker({value:this.value}).trigger('change')
		.on('change', function() {
			self.$emit('input', this.value);
		})
	},
	watch: {
		value: function (value) {
			$(this.$el).val(value);
        }
	},
	beforeDestroy: function() {
	    $(this.$el).datepicker('destroy');
	},
})
