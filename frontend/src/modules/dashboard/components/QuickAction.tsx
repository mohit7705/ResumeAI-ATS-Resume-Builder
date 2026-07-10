import Button from "../../../components/ui/Button";

type Props = {
  title: string;
  action: string;
};

export default function QuickAction({
  title,
  action,
}: Props) {

  function handleClick() {

    if (action === "generate") {
      window.location.href = "/resume";
    }

    if (action === "preview") {
      window.open(
        "http://127.0.0.1:8000/generated/html/resume.html",
        "_blank"
      );
    }

    if (action === "download") {
      window.open(
        "http://127.0.0.1:8000/generated/pdf/resume.pdf",
        "_blank"
      );
    }

  }


  return (
    <Button
      onClick={handleClick}
      style={{
        width: "100%",
        marginBottom: 10,
      }}
    >
      {title}
    </Button>
  );
}