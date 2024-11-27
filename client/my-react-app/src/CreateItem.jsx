import React from "react";

function CreateItem(props){
    const [item, setItem] = React.useState({
        title: "",
        category: "",
        description: "",
        id: Date.now()
    });
    function handleChange(e){
        setItem({...item, [e.target.name]: e.target.value});
    }
    function handleSubmit(e){
        props.addItem(item);
        setItem({title: "", category: "", description: "", id: Date.now()});
        e.preventDefault();
    }
    return ( 
        <div>
            <h3>Create New Item</h3>
            <form onSubmit={handleSubmit}>
                <input type="text" name="title" placeholder="Title" value={item.title} onChange={handleChange} />
                <input type="text" name="category" placeholder="Category" value={item.category} onChange={handleChange} />
                <textarea name="description" placeholder="Description" value={item.description} onChange={handleChange} />
                <button type="submit">Add Item</button>
            </form>
        </div>
    )
}

export default CreateItem;