/* setup the app object */
const app = new Vue({
    delimiters: ["[[", "]]"],
    el: "#app",
    data: {
    	risktypes: [],
        riskinstances: [],
        errors: [],
        riskinstance: null
    },
    watch: {
    	riskinstance: (val) => {
    		if (val === null) app.errors = [];
    	}
    },
    methods: {
    	update_riskinstances: function(continuation) {
        	axios.get(global.url_riskinstances).then((response) => {
        		app.riskinstances = response.data;
        		setTimeout(()=>{this.$forceUpdate();}, 50);
        	})
    	},
    	update_risktypes: function() {
        	axios.get(global.url_risktypes).then((response) => {
                app.risktypes = response.data;
                setTimeout(()=>{this.$forceUpdate();}, 50);
            });
    	},
        on_click_risktype: (risktype_id) => {
        	app.riskinstance = null;
        	axios.get(global.url_riskinstance_new + risktype_id + "/").then((response) => {
                app.riskinstance = response.data;
            });
        },
        on_click_riskinstance: (riskinstance_id) => {
        	app.riskinstance = null;
        	axios.get(global.url_riskinstance + riskinstance_id + "/").then((response) => {
	            app.riskinstance = response.data;
        	});
        },
        on_riskinstance_delete: function(riskinstance_id) {
        	let response = confirm("Delete Risk Instance?");
        	if (response) {
        		let delete_data = {ri_id: riskinstance_id};
        		axios.delete(global.url_riskinstance, {data:delete_data})
        		.then((response) => {
        			app.riskinstance = null;
        			app.update_riskinstances();
        		})
        		.catch((error) => {
        			let message = error.response.data.message? error.response.data.message:error.response.statusText;
        			alert('Could not delete risk instance due to the following issue:\n' + message);
        		})
        	}
        },
    	on_save: (riskinstance) => {
    		if (app.validate_form(riskinstance)) {
        		let post_data = app.riskinstance;
        		axios.post(global.url_riskinstance, post_data)
        		.then((response) => {
        			app.riskinstance = null;
        			app.update_riskinstances();
        		})
        		.catch((error) => {
        			let message = error.response.data.message? error.response.data.message:error.response.statusText;
        			alert('Could not save form due to the following issue:\n' + message);
        		})
    		}
    	},
    	on_cancel: () => {
    		app.riskinstance = null;
    	},
        validate_form: (riskinstance) => {
        	app.errors = [];
        	if ($.trim(String(riskinstance.title)) == "") {
        		app.errors.push(0);
        	}
        	for (let col of riskinstance.columns) {
        		let required = col.field.required;
        		let type = col.field.type.name;
        		let validator = new RegExp(col.field.type.regex_validator);
        		let value = col.value; 
        		if (type == 'Enum') {
        			value = value.value;
        			if (!value) value = "";
        		};
        		if ((String(value).match(validator) === null) || (required && $.trim(String(value)) == "")) {
        			app.errors.push(col.field.id);
        		}
        	}
        	return (app.errors.length == 0);
        },
        
    },
    mounted: function() {
    	this.update_risktypes();
    	this.update_riskinstances();
    }
});

