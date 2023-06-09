// function App() {
//     return (
// export const Foo = () => (
// <>
//   {"{"}% if not students %{"}"}
//   <p> У вас нет студентов </p>
//   {"{"}% else %{"}"}
//   <form
//     action="{{ url_for('api.add_students', Form_id='del') }}"
//     method="POST"
//     className="form-inline"
//   >
//     <label htmlFor="selecter" className="form-label">
//       Choose student:
//     </label>
//     <div className="select-wrapper">
//       <p>
//         <select
//           id="selecter"
//           className="form-select border border-warning border-opacity-50 w-50 mx-auto"
//           type="search"
//           list="character"
//           name="choose_student_for_del"
//           required=""
//         >
//           {"{"}% for student in students %{"}"}
//           <option value="{{ student[1] }}">
//             {"{"}
//             {"{"} student[0] {"}"}
//             {"}"}
//           </option>
//           {"{"}% endfor %{"}"}
//         </select>
//       </p>
//       <p>
//         <input
//           type="submit"
//           className="btn btn-signin w-25"
//           defaultValue="Delete"
//         />
//       </p>
//     </div>
//   </form>
//   {"{"}% endif %{"}"}
// </>
//   )

//   )
//   }

'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var students = "{{students}}";

var DelButton = function (_React$Component) {
    _inherits(DelButton, _React$Component);

    function DelButton() {
        _classCallCheck(this, DelButton);

        return _possibleConstructorReturn(this, (DelButton.__proto__ || Object.getPrototypeOf(DelButton)).apply(this, arguments));
    }

    _createClass(DelButton, [{
        key: 'render',
        value: function render() {
            return React.createElement(
                'div',
                null,
                students
            )
            // <div>
            //     for(var key in students){
            //         <div>{students[key]}</div>
            //     }

            //     <form action="{{ url_for('api.add_students', Form_id='del') }}" method="POST" className="form-inline">
            //         <label htmlFor="selecter" className="form-label">Choose student:</label>
            //         <div className="select-wrapper">
            //             <p><select id="selecter" className="form-select border border-warning border-opacity-50 w-50 mx-auto" type="search" list="character" name="choose_student_for_del" required>
            //                 {'{'}% for student in students %{'}'}
            //                 <option value="{{ student[1] }}">{'{'}{'{'} student[0] {'}'}{'}'}</option>
            //                 {'{'}% endfor %{'}'}
            //             </select></p>
            //             <p><input type="submit" className="btn btn-signin w-25" defaultValue="Delete" /></p>
            //         </div>
            //     </form>
            // </div>
            ;
        }
    }]);

    return DelButton;
}(React.Component);

var domContainer = document.querySelector('#del_button_container');
ReactDOM.render(React.createElement(DelButton, null), domContainer);