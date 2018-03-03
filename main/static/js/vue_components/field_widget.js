const error_msg = "This field is required or isn't valid.";

Vue.component("field_widget", {
    props: ["columns", "errors"],
    template:`
    <div class="field_widget">
	    <div v-for="col in columns">
	        <div class="field">
	            <span class="field_name">{{col.field.name}}</span>
	            <span v-bind:class="'required' + (col.field.required?'':' hidden')">*</span>
            	<div v-bind:class="'date_holder' + (errors.includes(col.field.id)?' invalid_field':'')">


			    	<!-- ************** 
			    	     *    TEXT    * 
			    	     ************** -->
		            <input v-if="col.field.type.name == 'Text'" class="form-control" 
		                   v-bind:name="col.field.name" type="text" v-model:value="col.value"/>


			        <!-- **************
			             *   NUMBER   *
			             ************** -->
	                <input v-else-if="col.field.type.name == 'Number'" class="form-control" 
	                       v-bind:name="col.field.name" type="number" v-model:value="col.value"/>

            
		            <!-- ************** 
		                 *    ENUM    * 
		                 ************** -->
					<div v-else-if="col.field.type.name == 'Enum'" class="field_enum">
	                    <div v-for="ev in col.field.enum_values">
	                    	<input type="radio" v-bind:name="col.field.name" v-bind:value="ev" 
	                               v-model:value="col.value"> <label>{{ev.value}}</label>
	                    </div>
                	</div>
    
            
		            <!-- ************** 
		                 *    DATE    * 
		                 ************** -->
                    <date_widget v-else-if="col.field.type.name == 'Date'" v-model:value="col.value"></date_widget>
              
              
    			</div>
                <span v-if="errors.includes(col.field.id)" class="error">{{error_msg}}</span>
            </div>
	    </div>
    </div>
    `,
    //updated: function() {$('input').val("");}
});
