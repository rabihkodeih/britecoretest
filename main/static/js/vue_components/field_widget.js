Vue.component("field_widget", {
    props: ["fields"],
    template:`
    <div class="field_widget">
	    <div v-for="field in fields">
	    	
	    	<!-- *** TEXT ***-->
	        <div v-if="field.type.name == 'Text'" class="field">
	            <span class="field_name">{{field.name}}</span>
	            <input class="form-control" v-bind:name="field.name" type="text" v-model:value="field.value"/>
	        </div>
	
	        <!-- *** NUMBER *** -->
	        <div v-else-if="field.type.name == 'Number'" class="field">
	            <span class="field_name">{{field.name}}</span>
	            <input class="form-control" v-bind:name="field.name" type="number" v-model:value="field.value"/>
	        </div>
	        
	        <!-- *** ENUM *** -->
	        <div v-else-if="field.type.name == 'Enum'" class="field">
	            <span class="field_name enum">{{field.name}}</span>
	            <span class="field_enum">
	                <div v-for="ev in field.enum_values">
	                    <input type="radio" v-bind:name="field.name" v-bind:value="ev" v-model:value="field.value"> <label>{{ev.value}}</label>
	                </div>
	            </span>
	        </div>
	
	        <!-- *** DATE *** -->
	        <div v-else-if="field.type.name == 'Date'" class="field">
	            <span class="field_name">{{field.name}}</span>
	            <div class="date_holder">
	       			<date_widget v-model:value="field.value"></date_widget>
	       		</div>
	        </div>
	        
	    </div>
    </div>
    `,
    //updated: function() {$('input').val("");}
});
