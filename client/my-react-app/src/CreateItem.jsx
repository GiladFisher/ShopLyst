import React from "react";

function CreateItem(props){
    const [item, setItem] = React.useState({
        title: "",
        category: "",
        description: "",
        id: Date.now()
    });

    function handleTitleBlur(e){
        if (e.target.value.trim() ){
            const value = e.target.value;
            fetch("http://127.0.0.1:5000/classify", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: value })
            })
            .then(res => res.json())
            .then(data => {
                if (data.category) {
                    setItem(prevItem => ({ ...prevItem, category: data.category }));
                }
            })
            .catch(err => console.error("Error fetching category:", err));
        }

    }

    function handleChange(e){
        setItem({...item, [e.target.name]: e.target.value});

        
    }
    function handleSubmit(e){
        props.addItem(item);
        setItem({title: "", category: "", description: "", id: Date.now()});
        e.preventDefault();
    }
    return ( 
        <div class="create_area">
            <h3>Create New Item</h3>
            <form onSubmit={handleSubmit}>
                <input type="text" name="title" placeholder="Title" value={item.title} onChange={handleChange} onBlur={handleTitleBlur} />
                <input type="text" name="category" placeholder="Category" value={item.category} onChange={handleChange} />
                <textarea name="description" placeholder="Description" value={item.description} onChange={handleChange} />
                <button id="additembutton" type="submit">Add Item</button>
            </form>
        </div>
    )
}

export default CreateItem;