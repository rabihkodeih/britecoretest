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
        	axios.get(global.url_riskinstance_new + risktype_id + "/").then(response => {
                app.riskinstance = response.data;
            });
        },
        on_click_riskinstance: (riskinstance_id) => {
        	app.riskinstance = null;
        	axios.get(global.url_riskinstance + riskinstance_id + "/").then(response => {
        		$('#ri-' + riskinstance_id).addClass('active');
	            app.riskinstance = response.data;
        	});
        },
    	on_save: (riskinstance) => {
    		//TODO: add form validation here
    		if (!app.validate_form(riskinstance)) {
    			console.log('you have validation errors');
    		} else {
//        		let post_data = app.risktype;
//        		axios.post(global.url_riskinstance, post_data)
//        		.then(response => {
//        			console.log(response); //TODO: dispaly a popup saying "Policy Saved"
//        		})
    		}
    	},
    	on_cancel: () => {
    		app.riskinstance = null;
    	},
        validate_form: (riskinstance) => {
        	//TODO: validate title
        	app.errors = [];
        	
        	//TODO: validate required (empty values)
        	for (let col of riskinstance.columns) {
        		let type = col.field.type.name;
        		let validator = new RegExp(col.field.type.regex_validator);
        		let required = col.field.required;
        		let value = col.value; 
        		if (type == 'Enum') {
        			value = value.value
        			if (!value) value = "";
        		};
        		
        		console.log(value);
        		console.log('-----------');
        		
        		if (String(value).match(validator) === null) {
        			app.errors.push(col.field.id);
        		}
        	}
        	
        	console.log(app.errors);
        	
        	return true;
        },
    },
    mounted: () => {
    	axios.get(global.url_risktypes).then(response => {
            app.risktypes = response.data;
        });
    	axios.get(global.url_riskinstances).then(response => {
    		app.riskinstances = response.data;
    	})
    }
});

