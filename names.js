import jinjaToJS from "jinja-to-js"; 
export default function templateFile(ctx) {
    var __result = "";
    var __tmp;
    var __runtime = jinjaToJS.runtime;
    var __filters = jinjaToJS.filters;
    var __globals = jinjaToJS.globals;
    var context = jinjaToJS.createContext(ctx);
    if (!__runtime.boolean(context.students)) { 
        __result += "\n	<p> У вас нет студентов </p>\n	"; 
    } else { 
        __result += "\n	<form action=\""; 
        __result += "" + __runtime.escape((__tmp = (context.url_for("api.add_students"))) == null ? "" : __tmp); 
        __result += "\" method=\"POST\"\n		class=\"form-inline\">\n		<label for=\"selecter\" class=\"form-label\">Choose student:</label>\n		<div class=\"select-wrapper\">\n			<p><select id=\"selecter\"\n					class=\"form-select border border-warning border-opacity-50 w-50 mx-auto\"\n					type=\"search\" list=\"character\" name=\"choose_student_for_del\" required>\n					<datalist id=\"character\">\n						"; __runtime.each(context.students, function (student) { var __$0 = context.student; context.student = student; __result += "\n						<option value=\""; __result += "" + __runtime.escape((__tmp = (student[1])) == null ? "" : __tmp); __result += "\">"; __result += "" + __runtime.escape((__tmp = (student[0])) == null ? "" : __tmp); __result += "</option>\n						"; context.student = __$0; }); __result += "\n					</datalist>\n				</select></p>\n			<p><input type=\"submit\" class=\"btn btn-signin w-25\" value=\"Delete\"></p>\n		</div>\n	</form>\n"; }
    return __result;
}