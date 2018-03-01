/* setup the app object */
const app = new Vue({
    delimiters: ["[[", "]]"],
    el: "#app",
    data: {
        risktypes: [],
        risktype: null
    },
    methods: {
        on_click: function(risktype_id) {
    		axios.get(global.url_risktype + risktype_id + "/").then(response => {
                this.risktype = response.data;
            });
        }
    },
    mounted: function() {
    	axios.get(global.url_risktypes).then(response => {
            this.risktypes = response.data;
        });
    }
});

