/* setup the app object */
const app = new Vue({
    delimiters: ["[[", "]]"],
    el: "#app",
    data: {
    	/* app state */
    	risktypes: [],
        riskinstances: [],
        
        /* working state */
        errors: [],
        riskinstance: null
    },
    watch: {
    	riskinstance: (val) => {
    		if (val === null) app.init_page();
    	}
    },
    methods: {
    	init_page: () => {
    		app.errors = [];
    		$('.ri-link').removeClass('active');
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
        		$('#ri-' + riskinstance_id).addClass('active');
	            app.riskinstance = response.data;
        	});
        },
    	on_save: (riskinstance) => {
    		if (app.validate_form(riskinstance)) {
        		let post_data = app.riskinstance;
        		axios.post(global.url_riskinstance, post_data)
        		.then((response) => {
        			console.log(response); 
        			//TODO: dispaly a popup saying "Policy Saved"
        			app.init_page();
        			app.riskinstance = null;
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
    mounted: () => {
    	axios.get(global.url_risktypes).then((response) => {
            app.risktypes = response.data;
        });
    	axios.get(global.url_riskinstances).then((response) => {
    		app.riskinstances = response.data;
    	})
    }
});

