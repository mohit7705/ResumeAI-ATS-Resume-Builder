import type { ReactNode } from "react";

type Props = {
  title?: string;
  description?: string;
  action?: ReactNode;
  footer?: ReactNode;
  children: ReactNode;
};

export default function Card({
  title,
  description,
  action,
  footer,
  children,
}: Props) {
  return (
    <section className="card">
      {(title || action) && (
        <header className="card__head">
          <div>
            {title && <h2 className="card__title">{title}</h2>}
            {description && <p className="card__desc">{description}</p>}
          </div>
          {action}
        </header>
      )}

      <div className="card__body">{children}</div>

      {footer && <footer className="card__foot">{footer}</footer>}
    </section>
  );
}
