---
name: angular-patterns
description: "Padrões Angular modernos: Standalone Components, Signals, inject(), HttpClient, RxJS, Testing. Use quando implementar features em Angular ou configurar projeto Angular."
---

# Angular — Patterns & Idioms

Padrões e idiomas para Angular moderno em produção (Standalone + Signals).

## Filosofia

- **Standalone Components**: sem NgModules — componentes auto-suficientes
- **Signals**: reatividade fine-grained, substituindo muitos usos de RxJS
- **inject() function**: DI funcional, sem constructor injection verbosa
- **Typed forms**: FormGroup/FormControl tipados nativamente
- **Control flow**: @if, @for, @switch nativos (não *ngIf/*ngFor)

## Estrutura de projeto

```
src/app/
├── core/              # Serviços singleton, guards, interceptors
│   ├── auth/
│   ├── http/
│   └── guards/
├── shared/            # Componentes, pipes, directives reutilizáveis
│   ├── components/
│   ├── pipes/
│   └── directives/
├── features/          # Feature modules (domínio)
│   └── orders/
│       ├── components/    # Componentes da feature
│       ├── services/      # Serviços da feature
│       ├── models/        # Interfaces/types
│       ├── routes.ts      # Rotas da feature
│       └── index.ts       # Public API
├── pages/             # Route components de nível superior
├── app.component.ts
├── app.config.ts      # provideRouter, provideHttpClient, etc.
└── app.routes.ts      # Rotas raiz
```

## Standalone Components

```typescript
// Componente standalone — sem NgModule
@Component({
  selector: "app-order-card",
  standalone: true,
  imports: [DatePipe, CurrencyPipe],
  template: `
    <article class="order-card">
      <h3>{{ order().title }}</h3>
      <p>Status: {{ order().status }}</p>
      <p>Total: {{ order().amount | currency }}</p>
      <p>Created: {{ order().createdAt | date: "medium" }}</p>
      <button type="button" (click)="cancel.emit(order().id)" [disabled]="order().status !== 'pending'">
        Cancel
      </button>
    </article>
  `,
})
export class OrderCardComponent {
  order = input.required<Order>();
  cancel = output<string>();
}
```

## Signals

```typescript
// Signals para estado reativo
@Component({
  selector: "app-order-list",
  standalone: true,
  imports: [OrderCardComponent],
  template: `
    <div class="filters">
      <select (change)="statusFilter.set($any($event.target).value)">
        <option value="">All</option>
        <option value="pending">Pending</option>
        <option value="completed">Completed</option>
      </select>
      <p>Showing {{ filteredOrders().length }} of {{ orders().length }} orders</p>
    </div>

    @for (order of filteredOrders(); track order.id) {
      <app-order-card [order]="order" (cancel)="onCancel($event)" />
    } @empty {
      <p>No orders found.</p>
    }
  `,
})
export class OrderListComponent {
  private orderService = inject(OrderService);

  orders = this.orderService.orders;
  statusFilter = signal<string>("");

  // computed — reage automaticamente a mudanças em orders() e statusFilter()
  filteredOrders = computed(() => {
    const filter = this.statusFilter();
    if (!filter) return this.orders();
    return this.orders().filter((o) => o.status === filter);
  });

  onCancel(id: string) {
    this.orderService.cancel(id);
  }
}
```

## Services com inject()

```typescript
@Injectable({ providedIn: "root" })
export class OrderService {
  private http = inject(HttpClient);
  private baseUrl = "/api/v1/orders";

  // Signal-based state
  private _orders = signal<Order[]>([]);
  orders = this._orders.asReadonly();

  loading = signal(false);
  error = signal<string | null>(null);

  loadOrders(filters?: OrderFilters): void {
    this.loading.set(true);
    this.error.set(null);

    this.http.get<Order[]>(this.baseUrl, { params: filters as any }).subscribe({
      next: (orders) => {
        this._orders.set(orders);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set(err.message);
        this.loading.set(false);
      },
    });
  }

  create(request: CreateOrderRequest): Observable<Order> {
    return this.http.post<Order>(this.baseUrl, request).pipe(
      tap((order) => this._orders.update((orders) => [order, ...orders])),
    );
  }

  cancel(id: string): void {
    this.http.patch<Order>(`${this.baseUrl}/${id}`, { status: "cancelled" }).subscribe({
      next: (updated) => {
        this._orders.update((orders) =>
          orders.map((o) => (o.id === id ? updated : o)),
        );
      },
    });
  }
}
```

## HttpClient + Interceptors

```typescript
// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding()),
    provideHttpClient(withInterceptors([authInterceptor, errorInterceptor])),
  ],
};

// Functional interceptor
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.token();

  if (token) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` },
    });
  }
  return next(req);
};

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        router.navigate(["/login"]);
      }
      return throwError(() => error);
    }),
  );
};
```

## Routing

```typescript
// app.routes.ts
export const routes: Routes = [
  { path: "", redirectTo: "orders", pathMatch: "full" },
  {
    path: "orders",
    loadChildren: () => import("./features/orders/routes").then((m) => m.ORDER_ROUTES),
  },
  {
    path: "login",
    loadComponent: () => import("./pages/login.component").then((m) => m.LoginComponent),
  },
];

// features/orders/routes.ts
export const ORDER_ROUTES: Routes = [
  { path: "", component: OrderListComponent },
  { path: ":id", component: OrderDetailComponent },
  {
    path: "create",
    component: CreateOrderComponent,
    canActivate: [authGuard],
  },
];

// Functional guard
export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  return auth.isAuthenticated() ? true : router.createUrlTree(["/login"]);
};
```

## Typed Reactive Forms

```typescript
@Component({
  selector: "app-create-order",
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <label for="title">Title</label>
      <input id="title" formControlName="title" />
      @if (form.controls.title.errors?.['required'] && form.controls.title.touched) {
        <span class="error">Title is required</span>
      }

      <label for="amount">Amount</label>
      <input id="amount" type="number" formControlName="amount" />
      @if (form.controls.amount.errors?.['min']) {
        <span class="error">Amount must be positive</span>
      }

      <button type="submit" [disabled]="form.invalid || submitting()">
        {{ submitting() ? "Creating..." : "Create" }}
      </button>
    </form>
  `,
})
export class CreateOrderComponent {
  private orderService = inject(OrderService);
  private router = inject(Router);

  submitting = signal(false);

  form = new FormGroup({
    title: new FormControl("", { nonNullable: true, validators: [Validators.required, Validators.maxLength(100)] }),
    amount: new FormControl(0, { nonNullable: true, validators: [Validators.required, Validators.min(0.01)] }),
    description: new FormControl("", { nonNullable: true }),
  });

  onSubmit(): void {
    if (this.form.invalid) return;
    this.submitting.set(true);

    this.orderService.create(this.form.getRawValue()).subscribe({
      next: () => this.router.navigate(["/orders"]),
      error: () => this.submitting.set(false),
    });
  }
}
```

## RxJS (quando usar)

```typescript
// Signals para: estado simples, computed values, UI state
// RxJS para: streams complexos, debounce, switchMap, combineLatest com timing

// Search com debounce — RxJS é o tool certo
@Component({ /* ... */ })
export class SearchComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();
  searchControl = new FormControl("", { nonNullable: true });

  ngOnInit() {
    this.searchControl.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap((query) => this.orderService.search(query)),
      takeUntil(this.destroy$),
    ).subscribe((results) => this.results.set(results));
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}

// toSignal / toObservable — bridge entre mundos
import { toSignal, toObservable } from "@angular/core/rxjs-interop";

const data = toSignal(this.http.get<Data[]>("/api/data"), { initialValue: [] });
const obs$ = toObservable(this.mySignal);
```

## Testing

```typescript
describe("OrderCardComponent", () => {
  it("should render order details", async () => {
    await render(OrderCardComponent, {
      componentInputs: { order: mockOrder },
    });

    expect(screen.getByText(mockOrder.title)).toBeInTheDocument();
    expect(screen.getByText(`Status: ${mockOrder.status}`)).toBeInTheDocument();
  });

  it("should emit cancel event", async () => {
    const cancelSpy = jest.fn();
    const { fixture } = await render(OrderCardComponent, {
      componentInputs: { order: { ...mockOrder, status: "pending" } },
      componentOutputs: { cancel: { emit: cancelSpy } as any },
    });

    await userEvent.click(screen.getByRole("button", { name: /cancel/i }));
    expect(cancelSpy).toHaveBeenCalledWith(mockOrder.id);
  });
});

// Service test com HttpClientTestingModule
describe("OrderService", () => {
  let service: OrderService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(OrderService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it("should load orders", () => {
    service.loadOrders();
    const req = httpMock.expectOne("/api/v1/orders");
    req.flush([mockOrder]);
    expect(service.orders()).toEqual([mockOrder]);
    expect(service.loading()).toBe(false);
  });

  afterEach(() => httpMock.verify());
});
```

## Checklist

- [ ] Standalone components (não NgModules)?
- [ ] Signals para estado reativo (não BehaviorSubject para estado simples)?
- [ ] inject() function (não constructor injection)?
- [ ] Control flow nativo (@if, @for, @switch — não *ngIf, *ngFor)?
- [ ] input()/output() signal-based (não @Input/@Output decorators)?
- [ ] Typed Reactive Forms?
- [ ] Functional interceptors e guards?
- [ ] Lazy loading de feature routes?
- [ ] RxJS apenas para streams complexos (debounce, switchMap)?
- [ ] takeUntil/DestroyRef para cleanup de subscriptions?
- [ ] Testing Library para testes de componente?
