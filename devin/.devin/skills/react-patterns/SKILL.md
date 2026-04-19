---
name: react-patterns
description: "Padrões React modernos: Hooks, React Query, Zustand, Testing Library, Vite, TypeScript. Use quando implementar features em React ou configurar projeto React."
argument-hint: "[contexto adicional]"
---

# React — Patterns & Idioms

Padrões e idiomas para React moderno em produção (Vite + TypeScript).

## Filosofia

- **Composição sobre herança**: componentes pequenos e compostos
- **Hooks como primitiva**: lógica reutilizável via custom hooks
- **Server state vs client state**: React Query para server, Zustand para client
- **Colocation**: manter código relacionado próximo

## Estrutura de projeto

```
src/
├── components/        # Componentes compartilhados (Button, Modal, etc.)
│   └── ui/           # Primitivos de UI
├── features/         # Feature modules (domínio)
│   └── orders/
│       ├── components/   # Componentes específicos da feature
│       ├── hooks/        # Custom hooks da feature
│       ├── api/          # React Query hooks (queries + mutations)
│       ├── types.ts      # Tipos da feature
│       └── index.ts      # Public API da feature
├── hooks/            # Hooks globais compartilhados
├── lib/              # Utilitários, configuração de libs
├── pages/            # Route components (ou routes/)
├── providers/        # Context providers
├── types/            # Tipos globais
└── main.tsx          # Entry point
```

## Componentes

```tsx
// Preferir function components com TypeScript
interface OrderCardProps {
  order: Order;
  onCancel: (id: string) => void;
}

function OrderCard({ order, onCancel }: OrderCardProps) {
  return (
    <article className="order-card">
      <h3>{order.title}</h3>
      <p>Status: {order.status}</p>
      <button
        type="button"
        onClick={() => onCancel(order.id)}
        disabled={order.status !== "pending"}
      >
        Cancel
      </button>
    </article>
  );
}

// Composição com children
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

function Card({ children, className }: CardProps) {
  return <div className={`card ${className ?? ""}`}>{children}</div>;
}
```

## Hooks

```tsx
// Custom hook para lógica reutilizável
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Hook com cleanup
function useEventListener(event: string, handler: (e: Event) => void) {
  const savedHandler = useRef(handler);

  useEffect(() => {
    savedHandler.current = handler;
  }, [handler]);

  useEffect(() => {
    const listener = (e: Event) => savedHandler.current(e);
    window.addEventListener(event, listener);
    return () => window.removeEventListener(event, listener);
  }, [event]);
}
```

## React Query (Server State)

```tsx
// api/orders.ts — queries e mutations
const orderKeys = {
  all: ["orders"] as const,
  lists: () => [...orderKeys.all, "list"] as const,
  list: (filters: OrderFilters) => [...orderKeys.lists(), filters] as const,
  details: () => [...orderKeys.all, "detail"] as const,
  detail: (id: string) => [...orderKeys.details(), id] as const,
};

function useOrders(filters: OrderFilters) {
  return useQuery({
    queryKey: orderKeys.list(filters),
    queryFn: () => fetchOrders(filters),
    staleTime: 5 * 60 * 1000, // 5 min
  });
}

function useOrder(id: string) {
  return useQuery({
    queryKey: orderKeys.detail(id),
    queryFn: () => fetchOrder(id),
    enabled: !!id,
  });
}

function useCreateOrder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createOrder,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: orderKeys.lists() });
    },
  });
}

// Uso no componente
function OrderList() {
  const [filters, setFilters] = useState<OrderFilters>({});
  const { data: orders, isLoading, error } = useOrders(filters);

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <ul>
      {orders?.map((order) => (
        <li key={order.id}>
          <OrderCard order={order} />
        </li>
      ))}
    </ul>
  );
}
```

## Zustand (Client State)

```tsx
// stores/useAuthStore.ts
interface AuthState {
  user: User | null;
  token: string | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  login: async (credentials) => {
    const { user, token } = await authApi.login(credentials);
    set({ user, token });
  },
  logout: () => set({ user: null, token: null }),
}));

// Uso — selector para evitar re-renders desnecessários
function UserMenu() {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  if (!user) return <LoginButton />;
  return <ProfileMenu user={user} onLogout={logout} />;
}
```

## Forms

```tsx
// React Hook Form (preferido para forms complexos)
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const orderSchema = z.object({
  title: z.string().min(1, "Title is required").max(100),
  amount: z.number().positive("Amount must be positive"),
  description: z.string().optional(),
});

type OrderFormData = z.infer<typeof orderSchema>;

function CreateOrderForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } =
    useForm<OrderFormData>({ resolver: zodResolver(orderSchema) });

  const createOrder = useCreateOrder();

  const onSubmit = (data: OrderFormData) => createOrder.mutateAsync(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <label htmlFor="title">Title</label>
      <input id="title" {...register("title")} aria-invalid={!!errors.title} />
      {errors.title && <span role="alert">{errors.title.message}</span>}

      <label htmlFor="amount">Amount</label>
      <input id="amount" type="number" {...register("amount", { valueAsNumber: true })} />
      {errors.amount && <span role="alert">{errors.amount.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Creating..." : "Create Order"}
      </button>
    </form>
  );
}
```

## Error Boundary

```tsx
import { ErrorBoundary, FallbackProps } from "react-error-boundary";

function ErrorFallback({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <pre>{error.message}</pre>
      <button type="button" onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <Routes />
    </ErrorBoundary>
  );
}
```

## Testing (Testing Library + Vitest)

```tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

// Wrapper para testes com providers
function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

describe("OrderCard", () => {
  it("renders order details", () => {
    render(<OrderCard order={mockOrder} onCancel={vi.fn()} />);
    expect(screen.getByText(mockOrder.title)).toBeInTheDocument();
    expect(screen.getByText(`Status: ${mockOrder.status}`)).toBeInTheDocument();
  });

  it("calls onCancel when cancel button clicked", async () => {
    const user = userEvent.setup();
    const onCancel = vi.fn();
    render(<OrderCard order={{ ...mockOrder, status: "pending" }} onCancel={onCancel} />);

    await user.click(screen.getByRole("button", { name: /cancel/i }));
    expect(onCancel).toHaveBeenCalledWith(mockOrder.id);
  });

  it("disables cancel for non-pending orders", () => {
    render(<OrderCard order={{ ...mockOrder, status: "completed" }} onCancel={vi.fn()} />);
    expect(screen.getByRole("button", { name: /cancel/i })).toBeDisabled();
  });
});

// Hook testing
import { renderHook, waitFor } from "@testing-library/react";

describe("useOrders", () => {
  it("fetches orders", async () => {
    const { result } = renderHook(() => useOrders({}), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toHaveLength(3);
  });
});
```

## MSW (Mock Service Worker)

```tsx
// mocks/handlers.ts
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/api/v1/orders", () => {
    return HttpResponse.json([
      { id: "1", title: "Order 1", status: "pending" },
    ]);
  }),

  http.post("/api/v1/orders", async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: "new-1", ...body }, { status: 201 });
  }),
];

// setup
import { setupServer } from "msw/node";
const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## Performance

```tsx
// React.memo — evita re-render quando props não mudam
const ExpensiveList = React.memo(function ExpensiveList({ items }: { items: Item[] }) {
  return <ul>{items.map((item) => <li key={item.id}>{item.name}</li>)}</ul>;
});

// useMemo — memoizar cálculos caros
function OrderSummary({ orders }: { orders: Order[] }) {
  const total = useMemo(
    () => orders.reduce((sum, o) => sum + o.amount, 0),
    [orders]
  );
  return <p>Total: {total}</p>;
}

// useCallback — estabilizar referências de funções
function Parent() {
  const handleClick = useCallback((id: string) => {
    // handler
  }, []);
  return <Child onClick={handleClick} />;
}

// Lazy loading de routes
const OrderDetails = lazy(() => import("./pages/OrderDetails"));
```

## Acessibilidade (a11y)

- Usar elementos semânticos (`button`, `nav`, `main`, `article`)
- Labels em todos os inputs (`<label htmlFor>` ou `aria-label`)
- `aria-invalid` e `role="alert"` para erros de form
- Keyboard navigation (`onKeyDown`, `tabIndex`)
- Skip links para navegação
- Contrast ratio mínimo 4.5:1

## Vite Config

```ts
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { "@": path.resolve(__dirname, "./src") },
  },
  server: {
    proxy: {
      "/api": { target: "http://localhost:8080", changeOrigin: true },
    },
  },
});
```

## Checklist

- [ ] Feature modules com colocation (componentes, hooks, API juntos)?
- [ ] React Query para server state (não useState para dados do servidor)?
- [ ] Query keys estruturadas e factory pattern?
- [ ] Zustand para client state (não prop drilling excessivo)?
- [ ] Forms com validação (Zod + React Hook Form)?
- [ ] Error Boundary para erros de renderização?
- [ ] Testes com Testing Library (queries por role/text, não por classe)?
- [ ] MSW para mock de API em testes?
- [ ] Lazy loading para route-level code splitting?
- [ ] Acessibilidade (semântica, labels, keyboard)?
