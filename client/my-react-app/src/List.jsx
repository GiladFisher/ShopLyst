import React from "react";
import CreateItem from "./CreateItem";
import ListItem from "./ListItem";


 function List(props){
    const [listItems, setListItems] = React.useState([]);
    function deleteItem(itemId){
        setListItems(prevItems => {
            return prevItems.filter(item => {return item.id !== itemId;});
        });
    }
    function addItem(newItem){
        setListItems(prevItems => {
            return [...prevItems, newItem];
        });
    }
    const sortedItems = [...listItems].sort((a, b) => {
        const categoryA = a.category.toLowerCase();
        const categoryB = b.category.toLowerCase();
        return categoryA.localeCompare(categoryB);
    });
    return(<div>
        <h1>{props.user.name}'s List</h1>
        <CreateItem addItem={addItem} />
        {sortedItems.map(item => <ListItem key={item.id} id={item.id}  item={item} deleteItem={deleteItem} />)}
    </div>)
 }

 export default List;