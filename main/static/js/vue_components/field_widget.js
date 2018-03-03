Vue.component("field_widget", {
    props: ["columns"],
    template:`
    <div class="field_widget">
	    <div v-for="col in columns">
	    	
	    	
	    	<!-- ************** 
	    	     *    TEXT    * 
	    	     ************** -->
	        <div v-if="col.field.type.name == 'Text'" class="field">
	            <span class="field_name">{{col.field.name}}</span>
	            <input class="form-control" v-bind:name="col.field.name" type="text" v-model:value="col.value"/>
	        </div>
	

            <!-- **************
                 *   NUMBER   *
                 ************** -->
            <div v-else-if="col.field.type.name == 'Number'" class="field">
                <span class="field_name">{{col.field.name}}</span>
                <input class="form-control" v-bind:name="col.field.name" type="number" v-model:value="col.value"/>
            </div>
            
            
            <!-- ************** 
                 *    ENUM    * 
                 ************** -->
            <div v-else-if="col.field.type.name == 'Enum'" class="field">
                <span class="field_name enum">{{col.field.name}}</span>
                <span class="field_enum">
                    <div v-for="ev in col.field.enum_values">
                    	<input type="radio" v-bind:name="col.field.name" v-bind:value="ev" 
                               v-model:value="col.value"> <label>{{ev.value}}</label>
                    </div>
                </span>
            </div>
    
            
            <!-- ************** 
                 *    DATE    * 
                 ************** -->
            <div v-else-if="col.field.type.name == 'Date'" class="field">
                <span class="field_name">{{col.field.name}}</span>
                <div class="date_holder">
                    <date_widget v-model:value="col.value"></date_widget>
                </div>
            </div>

	        
	    </div>
    </div>
    `,
    //updated: function() {$('input').val("");}
});
