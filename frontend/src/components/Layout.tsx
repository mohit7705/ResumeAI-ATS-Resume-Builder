import Sidebar from "./Sidebar";
import Header from "./Header";
import Content from "./Content";

export default function Layout() {
  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
      }}
    >
      <Sidebar />

      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Header />

        <Content />
      </div>
    </div>
  );
}