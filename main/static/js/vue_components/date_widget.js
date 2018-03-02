Vue.component("date_widget", {
	template: '<input class="form-control" type="text"/>',
	props: ['value'],
	mounted: function() {
		let self = this;
		//$(this.$el).datepicker({ minDate: startDate, value: startDate }).trigger('change')
		//TODO: replace by the above line and send {value: startDate} to datepicker widget
		//ref: http://gijgo.com/datepicker/example/vue-js
		$(this.$el).datepicker()
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
