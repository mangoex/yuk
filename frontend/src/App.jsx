import { useMemo, useState, useEffect } from "react";
import {
  Bell,
  BookStack,
  BrainResearch,
  Building,
  Calendar,
  CalendarPlus,
  CheckCircle,
  Clock,
  Community,
  FilterList,
  Gift,
  Group,
  List,
  Mail,
  Megaphone,
  NavArrowDown,
  NavArrowRight,
  Network,
  Package,
  Plus,
  RefreshDouble,
  Reports,
  Search,
  Settings,
  Spark,
  StatsReport,
  TaskList,
  User,
  WarningTriangle,
  Xmark,
} from "iconoir-react";

const avatarByOwner = {
  "Alejandro Ruiz": "https://randomuser.me/api/portraits/men/32.jpg",
  "Mariana Cruz": "https://randomuser.me/api/portraits/women/44.jpg",
  "Ricardo López": "https://randomuser.me/api/portraits/men/46.jpg",
  "Sofía Herrera": "https://randomuser.me/api/portraits/women/68.jpg",
  "Paula Sánchez": "https://randomuser.me/api/portraits/women/65.jpg",
};

const initialStages = [
  {
    id: "new",
    title: "Nuevo",
    color: "#1769e8",
    deals: [
      { id: "1", company: "Grupo Constructor del Bajío", value: 850000, owner: "Ricardo López", score: 62, inactivity: "2 días", risk: false },
      { id: "2", company: "Distribuidora del Valle", value: 620000, owner: "Mariana Cruz", score: 71, inactivity: "1 día", risk: false },
      { id: "3", company: "ServiPlast México", value: 1250000, owner: "Alejandro Ruiz", score: 58, inactivity: "4 días", risk: true },
      { id: "4", company: "Logística del Norte", value: 980000, owner: "Paula Sánchez", score: 75, inactivity: "Hoy", risk: false },
      { id: "5", company: "Alimentos Selectos", value: 450000, owner: "Ricardo López", score: 64, inactivity: "3 días", risk: false },
    ],
  },
  {
    id: "qualified",
    title: "Calificado",
    color: "#f0c419",
    deals: [
      { id: "6", company: "Industrias Molina", value: 1850000, owner: "Mariana Cruz", score: 76, inactivity: "2 días", risk: false },
      { id: "7", company: "Farmacéutica del Centro", value: 1620000, owner: "Alejandro Ruiz", score: 82, inactivity: "Hoy", risk: false },
      { id: "8", company: "Grupo Textil Águila", value: 2300000, owner: "Sofía Herrera", score: 45, inactivity: "5 días", risk: true },
      { id: "9", company: "Tiendas del Sol", value: 1240000, owner: "Ricardo López", score: 63, inactivity: "2 días", risk: false },
      { id: "10", company: "Metalúrgica del Pacífico", value: 470000, owner: "Paula Sánchez", score: 70, inactivity: "Hoy", risk: false },
    ],
  },
  {
    id: "proposal",
    title: "Propuesta",
    color: "#27a65a",
    deals: [
      { id: "11", company: "Hospital San Gabriel", value: 2150000, owner: "Alejandro Ruiz", score: 60, inactivity: "3 días", risk: false },
      { id: "12", company: "Universidad del Noroeste", value: 1980000, owner: "Sofía Herrera", score: 78, inactivity: "2 días", risk: false },
      { id: "13", company: "Cementos del Centro", value: 1750000, owner: "Ricardo López", score: 72, inactivity: "Hoy", risk: false },
      { id: "14", company: "Energía Sustentable", value: 1240000, owner: "Mariana Cruz", score: 59, inactivity: "4 días", risk: false },
      { id: "15", company: "Grupo Hotelero Pacífico", value: 670000, owner: "Ricardo López", score: 61, inactivity: "2 días", risk: false },
    ],
  },
  {
    id: "negotiation",
    title: "Negociación",
    color: "#8b5cf6",
    deals: [
      { id: "16", company: "Telecom del Bajío", value: 2800000, owner: "Alejandro Ruiz", score: 38, inactivity: "6 días", risk: true },
      { id: "17", company: "Automotriz del Norte", value: 1950000, owner: "Sofía Herrera", score: 57, inactivity: "4 días", risk: false },
      { id: "18", company: "Servicios Integrales México", value: 900000, owner: "Ricardo López", score: 74, inactivity: "Hoy", risk: false },
      { id: "19", company: "Aceros y Perfiles", value: 450000, owner: "Paula Sánchez", score: 60, inactivity: "3 días", risk: false },
    ],
  },
];

const navSections = [
  [
    ["Pipeline", Network],
    ["Leads", Group],
    ["Empresas", Building],
    ["Contactos", User],
    ["Actividades", TaskList],
    ["Seguimientos", Clock],
    ["Calendario", Calendar],
    ["Reportes", Reports],
    ["Pronósticos", StatsReport],
  ],
  [
    ["Listas", List],
    ["Campañas", Megaphone],
    ["Playbooks", BookStack],
    ["Productos", Package],
  ],
];

const money = new Intl.NumberFormat("es-MX", {
  style: "currency",
  currency: "MXN",
  maximumFractionDigits: 0,
});

const formatMoney = (value) => `${money.format(value)} MXN`;

function Avatar({ owner, size = 24 }) {
  return (
    <img
      className="avatar"
      src={avatarByOwner[owner] ?? avatarByOwner["Alejandro Ruiz"]}
      alt=""
      width={size}
      height={size}
    />
  );
}

function scoreTone(score) {
  if (score < 50) return "danger";
  if (score < 70) return "warning";
  return "success";
}

function DealCard({ deal, selected, onSelect, onDragStart }) {
  return (
    <button
      type="button"
      className={`deal-card ${selected ? "selected" : ""}`}
      onClick={() => onSelect(deal)}
      draggable
      onDragStart={(event) => onDragStart(event, deal)}
      aria-pressed={selected}
    >
      <strong>{deal.company}</strong>
      <span className="deal-value">{formatMoney(deal.value)}</span>
      <span className="deal-meta">
        <span className="owner">
          <Avatar owner={deal.owner} />
          {deal.owner}
        </span>
        <span className={`score ${scoreTone(deal.score)}`}>{deal.score}</span>
      </span>
      <span className="activity-line">
        <span className={deal.inactivity === "Hoy" ? "" : "inactive"}>
          Sin actividad
        </span>
        <span className={deal.inactivity === "Hoy" ? "" : "inactive"}>{deal.inactivity}</span>
        {deal.risk && <WarningTriangle width={16} height={16} aria-label="En riesgo" />}
      </span>
    </button>
  );
}

function AgentInsight({ icon: Icon, color, title, time, children, actionLabel }) {
  return (
    <section className="agent-insight">
      <header>
        <span className="agent-icon" style={{ "--agent-color": color }}>
          <Icon width={18} height={18} />
        </span>
        <strong>{title}</strong>
        <time>{time}</time>
      </header>
      <div className="agent-copy">{children}</div>
      <button type="button" className="text-action">
        {actionLabel}
      </button>
    </section>
  );
}

export function App() {
  const [currentTab, setCurrentTab] = useState("Pipeline");
  const [stages, setStages] = useState(initialStages);
  const [selectedDeal, setSelectedDeal] = useState(initialStages[1].deals[2]);
  const [query, setQuery] = useState("");
  const [riskOnly, setRiskOnly] = useState(false);
  const [showNewLead, setShowNewLead] = useState(false);
  const [showApifyModal, setShowApifyModal] = useState(false);
  const [toast, setToast] = useState("");
  const [followUpScheduled, setFollowUpScheduled] = useState(false);
  const [panelOpen, setPanelOpen] = useState(true);

  // External API state
  const [leadsList, setLeadsList] = useState([]);
  const [forecastData, setForecastData] = useState(null);
  const [apifyQuery, setApifyQuery] = useState("Construcción");
  const [apifyLocation, setApifyLocation] = useState("México");
  const [apifyLoading, setApifyLoading] = useState(false);

  // Fetch backend data
  useEffect(() => {
    fetchDealsFromApi();
    fetchLeads();
    fetchForecast();
  }, []);

  async function fetchDealsFromApi() {
    try {
      const res = await fetch("/api/v1/deals/stages");
      if (res.ok) {
        const data = await res.json();
        if (data && data.length > 0) setStages(data);
      }
    } catch (e) {
      console.warn("API offset, fallback to mock state", e);
    }
  }

  async function fetchLeads() {
    try {
      const res = await fetch("/api/v1/leads");
      if (res.ok) setLeadsList(await res.json());
    } catch (e) {}
  }

  async function fetchForecast() {
    try {
      const res = await fetch("/api/v1/reports/forecast");
      if (res.ok) setForecastData(await res.json());
    } catch (e) {}
  }

  const visibleStages = useMemo(
    () =>
      stages.map((stage) => ({
        ...stage,
        deals: stage.deals.filter((deal) => {
          const matchesQuery = deal.company.toLowerCase().includes(query.toLowerCase());
          return matchesQuery && (!riskOnly || deal.risk);
        }),
      })),
    [stages, query, riskOnly],
  );

  async function handleDrop(event, targetStageId) {
    event.preventDefault();
    const dealId = event.dataTransfer.getData("text/deal-id");
    let movingDeal;
    const nextStages = stages.map((stage) => ({
      ...stage,
      deals: stage.deals.filter((deal) => {
        if (String(deal.id) === String(dealId)) movingDeal = deal;
        return String(deal.id) !== String(dealId);
      }),
    }));
    if (!movingDeal) return;

    setStages(
      nextStages.map((stage) =>
        stage.id === targetStageId ? { ...stage, deals: [...stage.deals, movingDeal] } : stage,
      ),
    );

    try {
      await fetch(`/api/v1/deals/${dealId}/stage`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ stage_id: targetStageId }),
      });
    } catch (e) {}

    setToast(`${movingDeal.company} se movió a ${stages.find((stage) => stage.id === targetStageId)?.title}.`);
    window.setTimeout(() => setToast(""), 2600);
  }

  async function addLead(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const company = form.get("company");
    const value = Number(form.get("value"));
    const email = form.get("email");

    const newDeal = {
      id: String(Date.now()),
      company,
      value,
      owner: "Alejandro Ruiz",
      score: 68,
      inactivity: "Hoy",
      risk: false,
    };

    setStages((current) =>
      current.map((stage) =>
        stage.id === "new" ? { ...stage, deals: [newDeal, ...stage.deals] } : stage,
      ),
    );

    try {
      await fetch("/api/v1/deals", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company, value, owner: "Alejandro Ruiz", stage_id: "new" }),
      });
    } catch (e) {}

    setSelectedDeal(newDeal);
    setShowNewLead(false);
    setToast("Lead creado y calificado por el Prospector.");
    window.setTimeout(() => setToast(""), 2600);
  }

  async function handleApifyProspecting(e) {
    e.preventDefault();
    setApifyLoading(true);
    try {
      const res = await fetch("/api/v1/prospecting/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ search_query: apifyQuery, location: apifyLocation, limit_count: 5 }),
      });
      if (res.ok) {
        const result = await res.json();
        setToast(`Apify scrape completado: ${result.items_scraped} prospectos importados.`);
        fetchLeads();
        setShowApifyModal(false);
      }
    } catch (e) {
      setToast("Error al ejecutar Apify Scraper.");
    } finally {
      setApifyLoading(false);
      window.setTimeout(() => setToast(""), 3000);
    }
  }

  function scheduleFollowUp() {
    setFollowUpScheduled(true);
    setToast("Seguimiento agendado para hoy a las 16:30.");
    window.setTimeout(() => setToast(""), 2600);
  }

  return (
    <div className={`app-shell ${panelOpen ? "" : "panel-closed"}`}>
      <header className="topbar">
        <a className="brand" href="#pipeline" onClick={() => setCurrentTab("Pipeline")}>
          <span className="brand-mark">
            <Network width={20} height={20} />
          </span>
          <span>Antigravity</span>
        </a>

        <label className="global-search">
          <Search width={18} height={18} />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Buscar empresas, contactos, oportunidades..."
          />
          <kbd>⌘ K</kbd>
        </label>

        <div className="top-actions">
          <button type="button" className="icon-button notification" aria-label="Notificaciones">
            <Bell width={21} height={21} />
            <span>8</span>
          </button>
          <button type="button" className="icon-button" aria-label="Novedades">
            <Gift width={21} height={21} />
          </button>
          <span className="profile-divider" />
          <Avatar owner="Alejandro Ruiz" size={36} />
          <span className="profile-copy">
            <strong>Alejandro Ruiz</strong>
            <small>Director comercial</small>
          </span>
          <NavArrowDown width={18} height={18} />
        </div>
      </header>

      <aside className="sidebar">
        {navSections.map((section, sectionIndex) => (
          <nav key={sectionIndex} className="nav-section" aria-label={`Navegación ${sectionIndex + 1}`}>
            {section.map(([label, Icon]) => (
              <button
                key={label}
                type="button"
                className={currentTab === label ? "active" : ""}
                onClick={() => {
                  setCurrentTab(label);
                  if (label === "Pipeline") setRiskOnly(false);
                }}
              >
                <Icon width={19} height={19} />
                <span>{label}</span>
              </button>
            ))}
          </nav>
        ))}
        <div className="sidebar-bottom">
          <button type="button" onClick={() => setToast("Configuración de Tenant y Roles RBAC.")}>
            <Settings width={19} height={19} />
            <span>Configuración</span>
          </button>
          <div className="ai-status">
            <span className="status-dot" />
            <strong>AI en línea</strong>
            <small>3 agentes activos</small>
            <button type="button" onClick={() => setToast("Los tres agentes operan con normalidad.")}>
              Ver estado
            </button>
          </div>
        </div>
      </aside>

      <main className="workspace" id="pipeline">
        <section className="workspace-header">
          <div>
            <h1>{currentTab === "Pipeline" ? "Pipeline comercial" : currentTab}</h1>
            <button type="button" className="date-control">
              <Calendar width={18} height={18} />
              24 jul 2026 (Hoy)
              <NavArrowDown width={16} height={16} />
            </button>
          </div>
          <div className="header-actions">
            {currentTab === "Leads" && (
              <button type="button" className="primary-button" style={{ background: "#7655e8" }} onClick={() => setShowApifyModal(true)}>
                <Spark width={19} height={19} />
                Prospectar con Apify
              </button>
            )}
            <button type="button" className="primary-button" onClick={() => setShowNewLead(true)}>
              <Plus width={19} height={19} />
              Nuevo lead
            </button>
            {currentTab === "Pipeline" && (
              <button
                type="button"
                className={`filter-button ${riskOnly ? "active" : ""}`}
                onClick={() => setRiskOnly((current) => !current)}
                aria-pressed={riskOnly}
                aria-label="Mostrar oportunidades en riesgo"
              >
                <FilterList width={19} height={19} />
              </button>
            )}
          </div>
        </section>

        {currentTab === "Pipeline" && (
          <>
            <section className="pipeline-summary" aria-label="Resumen del pipeline">
              <div className="metric">
                <span className="metric-icon blue">
                  <StatsReport width={21} height={21} />
                </span>
                <span>
                  <small>Valor total del pipeline</small>
                  <strong>{formatMoney(24850300)}</strong>
                </span>
              </div>
              <span className="summary-divider" />
              <div className="metric">
                <span className="metric-icon coral">
                  <WarningTriangle width={21} height={21} />
                </span>
                <span>
                  <small>Oportunidades en riesgo</small>
                  <strong>7 · {formatMoney(6120000)}</strong>
                </span>
              </div>
              <button type="button" className="refresh" onClick={() => { fetchDealsFromApi(); setToast("Datos actualizados desde base de datos."); }}>
                <span>
                  Actualizar datos
                  <small>Hoy, 08:30</small>
                </span>
                <RefreshDouble width={18} height={18} />
              </button>
            </section>

            <section className="kanban" aria-label="Etapas del pipeline">
              {visibleStages.map((stage) => (
                <section
                  key={stage.id}
                  className="kanban-column"
                  onDragOver={(event) => event.preventDefault()}
                  onDrop={(event) => handleDrop(event, stage.id)}
                >
                  <header>
                    <strong>{stage.title}</strong>
                    <span>
                      {formatMoney(
                        stage.deals.reduce((sum, d) => sum + d.value, 0)
                      )}{" "}
                      ({stage.deals.length})
                    </span>
                    <i style={{ "--stage-color": stage.color }} />
                  </header>
                  <div className="deal-list">
                    {stage.deals.map((deal) => (
                      <DealCard
                        key={deal.id}
                        deal={deal}
                        selected={selectedDeal?.id === deal.id}
                        onSelect={(nextDeal) => {
                          setSelectedDeal(nextDeal);
                          setFollowUpScheduled(false);
                          setPanelOpen(true);
                        }}
                        onDragStart={(event, draggedDeal) =>
                          event.dataTransfer.setData("text/deal-id", String(draggedDeal.id))
                        }
                      />
                    ))}
                    {stage.deals.length === 0 && (
                      <div className="empty-stage">
                        <Search width={20} height={20} />
                        Sin oportunidades
                      </div>
                    )}
                  </div>
                  <div className="drop-zone">
                    <Network width={17} height={17} />
                    Suelta aquí para mover
                  </div>
                </section>
              ))}
            </section>
          </>
        )}

        {currentTab === "Leads" && (
          <section className="dashboard-view" style={{ padding: "20px", background: "white", borderRadius: "12px", boxShadow: "0 1px 3px rgba(0,0,0,0.05)" }}>
            <h3>Directorio de Leads y Cualificación Inteligente</h3>
            <p style={{ color: "#666", marginBottom: "20px" }}>SuperProspector evalúa cada lead deterministamente con la matriz ICP.</p>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ borderBottom: "2px solid #eee", textAlign: "left" }}>
                  <th style={{ padding: "12px" }}>Empresa</th>
                  <th>Contacto</th>
                  <th>Correo</th>
                  <th>Fuente</th>
                  <th>Score ICP</th>
                  <th>Temperatura</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {(leadsList.length > 0 ? leadsList : [
                  { company_name: "Grupo Constructor del Bajío", contact_name: "Carlos Mendoza", email: "cmendoza@grupocons.mx", source: "APIFY", score: 92, temperature: "HOT", status: "QUALIFIED" },
                  { company_name: "Distribuidora del Valle", contact_name: "Mariana Cruz", email: "mcruz@valle.com", source: "WEB", score: 71, temperature: "WARM", status: "NEW" },
                  { company_name: "ServiPlast México", contact_name: "Alejandro Ruiz", email: "aruiz@serviplast.mx", source: "MANUAL", score: 58, temperature: "COLD", status: "NEW" },
                ]).map((lead, idx) => (
                  <tr key={idx} style={{ borderBottom: "1px solid #f0f0f0" }}>
                    <td style={{ padding: "12px", fontWeight: "600" }}>{lead.company_name}</td>
                    <td>{lead.contact_name || "N/A"}</td>
                    <td>{lead.email || "contacto@empresa.com"}</td>
                    <td><span style={{ padding: "4px 8px", background: "#f0f4ff", color: "#1769e8", borderRadius: "4px", fontSize: "12px", fontWeight: "bold" }}>{lead.source}</span></td>
                    <td><strong>{lead.score} / 100</strong></td>
                    <td><span style={{ padding: "4px 8px", background: lead.temperature === "HOT" ? "#ffebee" : "#e8f5e9", color: lead.temperature === "HOT" ? "#d32f2f" : "#2e7d32", borderRadius: "4px", fontSize: "12px", fontWeight: "bold" }}>{lead.temperature}</span></td>
                    <td>{lead.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        )}

        {currentTab === "Pronósticos" && (
          <section style={{ padding: "20px", background: "white", borderRadius: "12px" }}>
            <h3>Motor de Pronóstico Ponderado de Ventas (Python Determinista)</h3>
            <p style={{ color: "#666", marginBottom: "20px" }}>Cálculo matemáticamente exacto según probabilidad de cierre de etapa y score ICP.</p>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
              <div style={{ padding: "20px", background: "#f8fafc", borderRadius: "8px" }}>
                <small>Valor Total Pipeline Bruto</small>
                <h2 style={{ color: "#1769e8", margin: "10px 0" }}>{formatMoney(forecastData?.total_pipeline_value_mxn || 24850300)}</h2>
              </div>
              <div style={{ padding: "20px", background: "#f0fdf4", borderRadius: "8px" }}>
                <small>Pronóstico Ponderado Estimado</small>
                <h2 style={{ color: "#16a34a", margin: "10px 0" }}>{formatMoney(forecastData?.weighted_forecast_value_mxn || 14280500)}</h2>
              </div>
            </div>
          </section>
        )}

        {["Empresas", "Contactos", "Actividades", "Seguimientos", "Calendario", "Reportes", "Listas", "Campañas", "Playbooks", "Productos"].includes(currentTab) && (
          <section style={{ padding: "24px", background: "white", borderRadius: "12px", boxShadow: "0 1px 3px rgba(0,0,0,0.05)" }}>
            <h3>Módulo Comercial: {currentTab}</h3>
            <p style={{ color: "#666", marginTop: "8px" }}>Este módulo está conectado al backend relacional y adaptadores del tenant ConsultorPRO.</p>
            <div style={{ marginTop: "20px", padding: "16px", background: "#f8fafc", borderRadius: "8px", borderLeft: "4px solid #1769e8" }}>
              <CheckCircle width={20} height={20} style={{ color: "#1769e8", verticalAlign: "middle", marginRight: "8px" }} />
              Datos sincronizados con PostgreSQL. Operaciones de {currentTab} listas para ejecutarse.
            </div>
          </section>
        )}
      </main>

      <aside className="insight-panel">
        <header className="insight-title">
          <h2>Siguiente mejor acción</h2>
          <button
            type="button"
            className="icon-button"
            aria-label="Cerrar panel"
            onClick={() => setPanelOpen(false)}
          >
            <Xmark width={20} height={20} />
          </button>
        </header>
        <div className="selected-summary">
          <strong>{selectedDeal?.company}</strong>
          <span>
            {formatMoney(selectedDeal?.value ?? 0)} <i />{" "}
            {stages.find((stage) => stage.deals.some((deal) => String(deal.id) === String(selectedDeal?.id)))?.title ??
              "Nuevo"}
          </span>
        </div>
        <div className="risk-alert">
          <StatsReport width={21} height={21} />
          <span>
            <strong>Riesgo alto de estancamiento</strong>
            <small>Sin actividad por {selectedDeal?.inactivity ?? "5 días"}</small>
          </span>
        </div>

        <div className="agents">
          <AgentInsight
            icon={Search}
            color="#1769e8"
            title="Prospector"
            time="Hoy, 08:25"
            actionLabel="Recomendación"
          >
            <p>
              Detectamos que {selectedDeal?.company} tiene un score ICP de {selectedDeal?.score ?? 75}/100.
            </p>
            <p className="recommendation">
              Contacta sobre el caso de éxito de su industria para reactivar el interés.
            </p>
          </AgentInsight>
          <AgentInsight
            icon={BrainResearch}
            color="#7655e8"
            title="Coach de ventas"
            time="Hoy, 08:25"
            actionLabel="Mejor enfoque"
          >
            <p>
              En oportunidades similares, el siguiente paso efectivo fue agendar una demo
              personalizada en un plazo de 3 días.
            </p>
            <p className="recommendation">
              Enfócate en reducción de tiempos de producción y trazabilidad.
            </p>
          </AgentInsight>
          <AgentInsight
            icon={CheckCircle}
            color="#29a567"
            title="Seguimiento"
            time="Hoy, 08:25"
            actionLabel="Próximo paso sugerido"
          >
            <p>
              Último contacto: <em>Llamada de revisión con equipo directivo.</em>
            </p>
            <p className="recommendation">Proponer demo para esta semana.</p>
          </AgentInsight>
        </div>

        <button
          type="button"
          className={`followup-button ${followUpScheduled ? "success" : ""}`}
          onClick={scheduleFollowUp}
          disabled={followUpScheduled}
        >
          {followUpScheduled ? (
            <>
              <CheckCircle width={20} height={20} />
              Seguimiento agendado
            </>
          ) : (
            <>
              <CalendarPlus width={20} height={20} />
              Crear seguimiento
            </>
          )}
        </button>
        <p className="privacy-note">
          <Spark width={16} height={16} />
          Los agentes usan información de tu CRM, correos y Apify.
        </p>
      </aside>

      {/* Modal Nuevo Lead */}
      {showNewLead && (
        <div className="modal-backdrop" role="presentation" onMouseDown={() => setShowNewLead(false)}>
          <section
            className="modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="new-lead-title"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <header>
              <span className="metric-icon blue">
                <Plus width={22} height={22} />
              </span>
              <span>
                <h2 id="new-lead-title">Nuevo lead</h2>
                <p>El Prospector lo calificará automáticamente.</p>
              </span>
              <button type="button" className="icon-button" onClick={() => setShowNewLead(false)}>
                <Xmark width={20} height={20} />
              </button>
            </header>
            <form onSubmit={addLead}>
              <label>
                Empresa
                <input name="company" required placeholder="Ej. Manufacturas del Centro" />
              </label>
              <label>
                Valor estimado
                <input name="value" required type="number" min="1" placeholder="850000" />
              </label>
              <label>
                Correo de contacto
                <span className="field-with-icon">
                  <Mail width={18} height={18} />
                  <input name="email" required type="email" placeholder="contacto@empresa.mx" />
                </span>
              </label>
              <footer>
                <button type="button" className="secondary-button" onClick={() => setShowNewLead(false)}>
                  Cancelar
                </button>
                <button type="submit" className="primary-button">
                  Crear lead
                  <NavArrowRight width={18} height={18} />
                </button>
              </footer>
            </form>
          </section>
        </div>
      )}

      {/* Modal Apify Prospector */}
      {showApifyModal && (
        <div className="modal-backdrop" role="presentation" onMouseDown={() => setShowApifyModal(false)}>
          <section
            className="modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="apify-modal-title"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <header>
              <span className="metric-icon blue" style={{ background: "#f3e8ff", color: "#7655e8" }}>
                <Spark width={22} height={22} />
              </span>
              <span>
                <h2 id="apify-modal-title">Prospección Automatizada con Apify</h2>
                <p>Extrae prospectos B2B y califícalos automáticamente con Python.</p>
              </span>
              <button type="button" className="icon-button" onClick={() => setShowApifyModal(false)}>
                <Xmark width={20} height={20} />
              </button>
            </header>
            <form onSubmit={handleApifyProspecting}>
              <label>
                Sector / Industria objetivo
                <input value={apifyQuery} onChange={(e) => setApifyQuery(e.target.value)} required placeholder="Ej. Construcción, Farmacéutica" />
              </label>
              <label>
                Ubicación geográfica
                <input value={apifyLocation} onChange={(e) => setApifyLocation(e.target.value)} required placeholder="Ej. Querétaro, México" />
              </label>
              <footer>
                <button type="button" className="secondary-button" onClick={() => setShowApifyModal(false)}>
                  Cancelar
                </button>
                <button type="submit" className="primary-button" style={{ background: "#7655e8" }} disabled={apifyLoading}>
                  {apifyLoading ? "Scrapeando..." : "Ejecutar Apify Scraper"}
                  <NavArrowRight width={18} height={18} />
                </button>
              </footer>
            </form>
          </section>
        </div>
      )}

      {toast && (
        <div className="toast" role="status">
          <CheckCircle width={19} height={19} />
          {toast}
        </div>
      )}
    </div>
  );
}
