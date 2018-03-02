/* setup the app object */
const app = new Vue({
    delimiters: ["[[", "]]"],
    el: "#app",
    data: {
        risktypes: [],
        risktype: null
    },
    methods: {
        on_click_risktype: (risktype_id) => {
        	axios.get(global.url_risktype + risktype_id + "/").then(response => {
                app.risktype = response.data;
            });
        },
    	on_save_form: (risktype_id) => {
    		let post_data = app.risktype;
    		axios.post(global.url_riskinstance, post_data)
    		.then(response => {
    			console.log(response); //TODO: make error check using response object
    		})
//    		.catch(error => {
//    			console.log(error); //TODO: handle errors gracefully
//    		})
    	},
    	on_cancel_form: () => {
    		app.risktype = null;
    	}
    },
    mounted: () => {
    	axios.get(global.url_risktypes).then(response => {
            app.risktypes = response.data;
        });
    }
});

