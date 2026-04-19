---
name: angularjs-migration
description: "Migração AngularJS para Angular: estratégia incremental, ngUpgrade, dual-boot, padrões de coexistência. Use quando planejar ou executar migração de AngularJS (1.x) para Angular moderno."
argument-hint: "[contexto adicional]"
---

# AngularJS → Angular Migration

Estrategia e padroes para migracao incremental de AngularJS (1.x) para Angular moderno.

## Estrategias de migracao

| Estrategia | Risco | Tempo | Quando usar |
|------------|-------|-------|-------------|
| **Big Bang** | Alto | Curto | App pequena (< 20 componentes) |
| **Incremental (ngUpgrade)** | Baixo | Longo | App grande em producao |
| **Strangler Fig** | Baixo | Medio | Novas features em Angular, legado coexiste |
| **Rewrite** | Alto | Longo | Divida tecnica extrema, app instavel |

**Recomendacao para sistemas criticos**: Incremental (ngUpgrade) ou Strangler Fig.

## Preparacao (antes de migrar)

### 1. Modernizar o AngularJS

```javascript
// ANTES: controller + scope (legado)
angular.module('app').controller('OrderCtrl', function($scope, OrderService) {
    $scope.orders = [];
    $scope.loadOrders = function() {
        OrderService.list().then(function(orders) {
            $scope.orders = orders;
        });
    };
});

// DEPOIS: component + controllerAs (moderno)
angular.module('app').component('orderList', {
    template: `
        <div>
            <div ng-repeat="order in $ctrl.orders track by order.id">
                {{order.title}} - {{order.status}}
            </div>
        </div>
    `,
    controller: class OrderListController {
        constructor(OrderService) {
            'ngInject';
            this.OrderService = OrderService;
            this.orders = [];
        }

        $onInit() {
            this.loadOrders();
        }

        loadOrders() {
            this.OrderService.list().then(orders => {
                this.orders = orders;
            });
        }
    }
});
```

### 2. Adotar TypeScript no AngularJS

```typescript
// service em TypeScript
export class OrderService {
    static $inject = ['$http'];

    constructor(private $http: ng.IHttpService) {}

    list(): ng.IPromise<Order[]> {
        return this.$http.get<Order[]>('/api/v1/orders').then(res => res.data);
    }
}

angular.module('app').service('OrderService', OrderService);
```

### 3. Checklist pre-migracao

- [ ] Components em vez de directives com scope isolado?
- [ ] controllerAs em vez de $scope?
- [ ] Lifecycle hooks ($onInit, $onDestroy) em vez de link function?
- [ ] TypeScript adotado?
- [ ] Services com class syntax?
- [ ] Build moderno (Webpack/Vite)?
- [ ] Testes existentes (para validar migracao)?
- [ ] One-way binding (`<`) em vez de two-way (`=`)?

## ngUpgrade — Dual boot

### Setup

```typescript
// main.ts — bootstrap hibrido
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { UpgradeModule } from '@angular/upgrade/static';

@NgModule({
  imports: [BrowserModule, UpgradeModule],
  declarations: [/* Angular components */],
})
export class AppModule {
  constructor(private upgrade: UpgradeModule) {}

  ngDoBootstrap() {
    // Bootstrap AngularJS dentro do Angular
    this.upgrade.bootstrap(document.body, ['app'], { strictDi: true });
  }
}

platformBrowserDynamic().bootstrapModule(AppModule);
```

### Usar componente Angular no AngularJS

```typescript
// Angular component
@Component({
  selector: 'app-order-card',
  standalone: true,
  template: `
    <div class="order-card">
      <h3>{{ order.title }}</h3>
      <p>Status: {{ order.status }}</p>
    </div>
  `,
})
export class OrderCardComponent {
  @Input() order!: Order;
}

// Downgrade para AngularJS
import { downgradeComponent } from '@angular/upgrade/static';

angular.module('app').directive('appOrderCard',
  downgradeComponent({ component: OrderCardComponent })
);
```

```html
<!-- Uso no template AngularJS -->
<app-order-card [order]="$ctrl.selectedOrder"></app-order-card>
```

### Usar service AngularJS no Angular

```typescript
// Upgrade de service AngularJS para injetar no Angular
import { InjectionToken } from '@angular/core';

export const ORDER_SERVICE = new InjectionToken<any>('OrderService');

// No modulo
@NgModule({
  providers: [{
    provide: ORDER_SERVICE,
    useFactory: (injector: any) => injector.get('OrderService'),
    deps: ['$injector'],
  }],
})
export class AppModule {}

// Uso no Angular component
@Component({ /* ... */ })
export class OrderListComponent {
  constructor(@Inject(ORDER_SERVICE) private orderService: any) {}
}
```

### Usar service Angular no AngularJS

```typescript
// Downgrade de service Angular
import { downgradeInjectable } from '@angular/upgrade/static';

@Injectable({ providedIn: 'root' })
export class NewOrderService {
  constructor(private http: HttpClient) {}
  list(): Observable<Order[]> {
    return this.http.get<Order[]>('/api/v1/orders');
  }
}

angular.module('app').factory('NewOrderService',
  downgradeInjectable(NewOrderService)
);
```

## Strangler Fig — Roteamento hibrido

```typescript
// Angular routes para novas features
const routes: Routes = [
  { path: 'orders', component: OrderListComponent },        // Angular (novo)
  { path: 'orders/:id', component: OrderDetailComponent },  // Angular (novo)
  // Rotas legadas continuam no ui-router do AngularJS
];

// AngularJS route para "catch-all" do legado
$stateProvider.state('legacy', {
  url: '/{path:.*}',
  template: '<legacy-app></legacy-app>',
});
```

## Ordem de migracao recomendada

```
1. Servicos utilitarios (formatacao, validacao) — sem UI
2. Componentes "folha" (sem filhos) — OrderCard, StatusBadge
3. Servicos de dados (HTTP services) — OrderService
4. Componentes compostos — OrderList, OrderForm
5. Rotas/paginas inteiras — /orders, /orders/:id
6. Layout e navegacao — header, sidebar, router
7. Bootstrap — remover AngularJS completamente
```

### Criterio de migracao por componente

| Criterio | Migrar agora | Migrar depois |
|----------|-------------|--------------|
| Feature nova sendo adicionada | Sim | — |
| Bug critico no componente | Sim | — |
| Componente estavel sem mudancas | — | Sim |
| Componente com muitas dependencias AngularJS | — | Sim |
| Componente compartilhado por muitas paginas | Sim (alto impacto) | — |

## Armadilhas comuns

| Armadilha | Solucao |
|-----------|---------|
| Digest cycle mismatch | Usar `NgZone.run()` quando chamar Angular de AngularJS |
| Rotas conflitantes | Definir boundary clara — novas rotas em Angular, legado em ui-router |
| Bundle size explode | Lazy loading de modulos Angular, tree-shaking |
| Testes quebram | Manter testes de cada mundo separados (Karma para AJS, Jest para Angular) |
| Performance degrada | Dual-boot tem overhead — monitorar e migrar mais rapido |

## Metricas de progresso

```
Total de componentes: 150
Migrados para Angular: 45 (30%)
Em dual-boot: 150 (100% — tudo funciona junto)
AngularJS removido: 0% (meta: 100%)

Meta: migrar 5-10 componentes por sprint
Deadline: remover AngularJS em 6 meses
```

## Checklist

- [ ] AngularJS modernizado (components, controllerAs, TypeScript)?
- [ ] Build system suporta dual-boot (Webpack/Vite)?
- [ ] ngUpgrade configurado e funcionando?
- [ ] Ordem de migracao definida (folha → raiz)?
- [ ] Testes existentes passando antes e depois de cada migracao?
- [ ] Metricas de progresso trackeadas?
- [ ] Rotas claramente separadas (Angular vs AngularJS)?
- [ ] Performance monitorada (dual-boot tem overhead)?
- [ ] Plano para remover AngularJS completamente?
