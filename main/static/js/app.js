/* setup the app object */
const app = new Vue({
    delimiters: ["[[", "]]"],
    el: "#app",
    data: {
        risktypes: [],
        riskinstances: [],
        riskinstance: null
    },
    methods: {
        on_click_risktype: (risktype_id) => {
        	axios.get(global.url_riskinstance_new + risktype_id + "/").then(response => {
                app.riskinstance = response.data;
            });
        },
        on_click_riskinstance: (riskinstance_id) => {
          	axios.get(global.url_riskinstance + riskinstance_id + "/").then(response => {
	            app.riskinstance = response.data;
	        });
        },
    	on_save_policy: (riskinstance) => {
    		console.log(app.riskinstance);
//    		let post_data = app.risktype;
//    		axios.post(global.url_riskinstance, post_data)
//    		.then(response => {
//    			console.log(response); //TODO: dispaly a popup saying "Policy Saved"
//    		})
    	},
    	on_cancel_policy: () => {
    		app.riskinstance = null;
    	}
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

