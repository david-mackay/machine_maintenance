import React, {useState} from 'react';
import ReactDOM from 'react-dom';
import {useForm} from 'react-hook-form';
import placeholder from './placeholder.jpg';
import mongoose from 'mongoose';
import "../utilities.css";
const MachineSchema = new mongoose.Schema({
  part1: Boolean,
  part2: Boolean,
  part3: Boolean,
  part4: Boolean,
  part5: Boolean,
  date_maintained: Date,
  notes: String,
})

const Maintenance = mongoose.model("Machine", MachineSchema)
// mongoDb password = unitedplastics_admin123
function App(){
  return (
  <Navbar>

    <NavItem text = "Machines" icon = "🔽">
      <DropdownMenu></DropdownMenu>
    </NavItem>
    
    
  </Navbar>


  );
}

function DropdownMenu(){
  const [open, setOpen] = useState(false);


   function DropdownItem(props){
    
    return(
      <a href = "#" className = "menu-item" onClick={() => ReactDOM.render(props.form, document.getElementById("form"))} >
        <span className = "icon-button" >{props.text}</span>
        {props.children}
      </a>

    );
  }


  return (
    <div className = "dropdown">
      <DropdownItem text = "H-111 Front" form = {MachineForm( "H-111 Front")} ></DropdownItem>
      <DropdownItem text = "H-111 Rear" form = {MachineForm( "H-111 Rear")}></DropdownItem>
      <DropdownItem text = "H-111 Re-Built" form = {MachineForm( "H-111 Re-Built")}></DropdownItem>
      <DropdownItem text = "FHB-106" form = {MachineForm( "FHB-106")}></DropdownItem>
      <DropdownItem text = "O54" form = {MachineForm( "O54")}></DropdownItem>
      <DropdownItem text = "H-121" form = {MachineForm( "H-121")}></DropdownItem>
      <DropdownItem text = "BA-15" form = {MachineForm( "BA-15")}></DropdownItem>
    </div>
  );
 
}

function Navbar(props){
  return(
    <nav className = "navbar">
      <ul className = "navbar-nav">{props.children}</ul>
    </nav>
  );
}

function NavItem(props){
  const [open, setOpen] = useState(false);
  return(
      <li className = 'navitem'>
        <a href = "#" className = "icon-button" onClick = { () => setOpen(!open)}>
          {props.text + props.icon}
        </a>
        {open && props.children}
      </li>
  );
}

function MachineForm(text){
  const {register, handleSubmit, formState: {errors}} = useForm();

  const onSubmit = data => {
    console.log(data)
    // let machine = new Maintenance(data);
    // machine.save()
    
  }


  return(
    <div>
      <h1>{text}</h1><br/><br/>
      <img src = {placeholder}/>  
      <form method = "post" onSubmit = {handleSubmit(onSubmit)}>
        <label>Part 1</label>
        <input type = "checkbox" {...register("part1")}></input><br/>
        <label>Part 2</label>
        <input type = "checkbox" {...register("part2")}></input><br/>
        <label>Part 3</label>
        <input type = "checkbox" {...register("part3")}></input><br/>
        <label>Part 4</label>
        <input type = "checkbox" {...register("part4")}></input><br/>
        <label>Part 5</label>
        <input type = "checkbox" {...register("part5")}></input><br/>

        <label>Date Maintained</label><br/>
        <input type = "date" className = "d" {...register("date_maintained", {required: true})}></input><br/>
        {errors.date_maintained && <p>"Maintenance Date is required"</p>}
        

        <label>Notes</label><br/>
        <textarea  cols="30" rows="10" {...register("notes")}></textarea><br/>

        <input type = "submit" className = "submitbutton"></input>
      </form>
    </div>


  );
}



export default App;