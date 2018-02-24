/* define components */

Vue.component("date_widget", {
	template: '<input class="form-control" type="text"/>',
	mounted: function() {
		$(this.$el).datepicker();
	},
	beforeDestroy: function() {
	    $(this.$el).datepicker('destroy');
	},
})

Vue.component("field_widget", {
    props: ["fields"],
    template:`
    <div class="field_widget">
	    <div v-for="field in fields">
	    	
	    	<!-- *** TEXT ***-->
	        <div v-if="field.type.name == 'Text'" class="field">
	            <span class="field_name">{{field.name}}</span>
	            <input class="form-control" type="text"/>
	        </div>
	
	        <!-- *** NUMBER *** -->
	        <div v-else-if="field.type.name == 'Number'" class="field">
	            <span class="field_name">{{field.name}}</span>
	            <input class="form-control" type="number"/>
	        </div>
	        
	        <!-- *** ENUM *** -->
	        <div v-else-if="field.type.name == 'Enum'" class="field">
	            <span class="field_name enum">{{field.name}}</span>
	            <span class="field_enum">
	                <div v-for="ev in field.enum_values">
	                    <input type="radio" v-bind:name="field.name" v-bind:value="ev"> <label>{{ev.value}}</label>
	                </div>
	            </span>
	        </div>
	
	        <!-- *** DATE *** -->
	        <div v-else-if="field.type.name == 'Date'" class="field">
	            <span class="field_name">{{field.name}}</span>
	            <div class="date_holder">
	       			<date_widget></date_widget>
	       		</div>
	        </div>
	        
	    </div>
    </div>
    `,
    updated: function() {
    	$('input').val("");
    }
});



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

