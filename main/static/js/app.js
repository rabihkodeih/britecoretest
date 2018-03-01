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
    		console.log(risktype_id);
    		console.log(app.risktype);
    		console.log(global.url_risktype)
    		//app.risktype = null;
    		//let post_data = {first:'Rabih', last:'Kodeih'};
    		let post_data = app.risktype;
    		axios.post(global.url_risktype, post_data)
    		.then(response => {
    			console.log(response); //TODO: make error check using response object
    		})
    		.catch(error => {
    			console.log(error); //TODO: handle errors gracefully
    		})
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

