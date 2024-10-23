import './App.css';

function Textbox() {
  return (
    <form>
  <textarea class="textarea white bg-gray" placeholder="Write something.."></textarea>
    </form>
  );
}

function Messaging() {
  return(
    <div class="messaging bg-white"></div>
  );
}

export default function MyApp() {
  return (
    <div>
      <h1 class="MyApp white">Alissaa</h1>
      <Messaging />
      <Textbox />
      <input type="submit" value="Submit"></input>
    </div>
  );
}